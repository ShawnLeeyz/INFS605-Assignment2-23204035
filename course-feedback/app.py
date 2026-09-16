
"""
Handles submitting and retrieving student feedback about courses.
Has its own database (feedback-db). Calls student-profile and
course-catalogue over HTTP to check a student_id/course_id exists
before accepting feedback.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import requests
import os
import time

app = Flask(__name__) # Tell Flask to use this file as the main application
CORS(app)             # Enable CORS for all routes

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://feedbackuser:feedbackpass@feedback-db:5432/feedbackdb"
)

# Addresses of the other services to validate course id and student id
STUDENT_SERVICE_URL = os.getenv("STUDENT_SERVICE_URL", "http://student-profile:5001")
COURSE_SERVICE_URL = os.getenv("COURSE_SERVICE_URL", "http://course-catalogue:5002")

# Address of the notification service to send notifications when feedback is submitted
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification:5004")

# -----------------------------
# Wait-and-retry for database
# -----------------------------
# When containers start, Postgres may take a few seconds to become ready.
# This loop tries to connect multiple times before giving up (useful in Docker).
max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB!")
        conn.close()
        break
    except psycopg2.OperationalError:
        # If the connection failed, wait and try again.
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    # If we've retried max_retries times, raise an error and stop the service.
    raise Exception(f"Could not connect to the database after {max_retries} retries")

# Return a new database connection
def get_connection():
    return psycopg2.connect(DATABASE_URL)

# -----------------------------
# Simple health endpoint
# -----------------------------
@app.route("/")
def home():
    """
    Health check and human-readable message.
    Frontend or a human tester can hit this endpoint to confirm the service is running.
    """
    return (
        "Hello from course-feedback service (with Postgres DB)! "
        "This is a line of text to let you know that the API service is running smoothly with full CRUD capability"
    )

# -----------------------------
# Validation functions
# -----------------------------

#This method checks if a student exists
def student_exist(student_id):
    try:
        response = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

#This method checks if a course exsists
def course_exist(course_id):
    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/courses/{course_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# -----------------------------
# GET /feedback - Get all feedback
# -----------------------------
@app.route("/feedback", methods=["GET"])
def get_feedback():

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, course_id, student_id, comment, category, created_at FROM feedback ORDER BY created_at DESC")

    rows = cur.fetchall()
    cur.close()
    conn.close()

    feedback = [{"id": row[0], "course_id": row[1], "student_id": row[2], "comment": row[3], "category": row[4], "created_at": row[5]   } for row in rows]

    return jsonify(feedback), 200

# -----------------------------
# POST /feedback - Submit new feedback
# -----------------------------
@app.route("/feedback", methods=["POST"])
def create_feedback():

    #Getting the data from the request
    data = request.get_json() or {}
    student_id = data.get("student_id")
    course_id = data.get("course_id")
    category = data.get("category")
    comment = data.get("comment")

    # Check if all the fields have been provided
    if not all([student_id, course_id, category, comment]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the student actually exists
    if not student_exist(student_id):
        return jsonify({"error": "Student does not exist"}), 404

    # CHeck if the course actually exists
    if not course_exist(course_id):
        return jsonify({"error": "Course does not exist"}), 404

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("INSERT INTO feedback (student_id, course_id, category, comment) VALUES (%s, %s, %s, %s) RETURNING id", (student_id, course_id, category, comment))
    feedback_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    # This try-except block is use to notify the student that the feedback has been submitted
    try:
        requests.post(f"{NOTIFICATION_SERVICE_URL}/notification", json={
            "student_id": student_id,
            "message": f"Feedback successfully submited"
        })
    except requests.exceptions.RequestException:
        pass

    return jsonify({"message": "Feedback succefully created", "feedback_id": feedback_id}), 201

# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)