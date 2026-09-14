from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__) # Tell Flask to use this file as the main application
CORS(app)             # Enable CORS for all routes

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://courseuser:coursepass@course-db:5432/coursedb"
)
# docker compose up -d --build course-catalogue
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
        "Hello from course-catalogue service (with Postgres DB)! "
        "This is a line of text to let you know that the API service is running smoothly with full CRUD capability"
    )

# -------------------------------------------
# GET /courses - Get all course
# -------------------------------------------
# Example:
# curl http://localhost:5002/courses
@app.route("/courses", methods=["GET"])
def get_courses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    courses = [{"id": row[0], "course_code": row[1], "course_name": row[2], "description": row[3], "credits": row[4]} for row in rows]
    return jsonify(courses), 200

# -------------------------------------------
# GET /courses/<id> - Get a single course
# -------------------------------------------
# Example:
# curl http://localhost:5002/courses/1
@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Course not found"}), 404

    course = {"id": row[0], "course_code": row[1], "course_name": row[2], "description": row[3], "credits": row[4]}
    return jsonify(course), 200

# -------------------------------------------
# POST /courses - Create a new course
# -------------------------------------------
# Example:
# curl -X POST http://localhost:5002/courses -H "Content-Type: application/json" -d '{"course_code": "CS104", "course_name": "Introduction to Computer Science", "description": "Learn the basics of computer science.", "credits": 3}'
@app.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json()
    course_code = data.get("course_code")
    course_name = data.get("course_name")
    description = data.get("description")
    credits = data.get("credits")

    # Check if the required fields are present
    if not all([course_code, course_name, description, credits]):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate that credits is a positive integer
    if not isinstance(credits, int) or credits <= 0:
        return jsonify({"error": "Credits must be a positive integer"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Check if course_code already exists in the database
    cur.execute("SELECT id FROM courses WHERE course_code = %s", (course_code,))
    existing = cur.fetchone()

    if existing:
        cur.close()
        conn.close()
        return jsonify({"error": "Course code already exists"}), 409

    cur.execute(
        "INSERT INTO courses (course_code, course_name, description, credits) VALUES (%s, %s, %s, %s) RETURNING id",
        (course_code, course_name, description, credits)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": new_id}), 201

# -------------------------------------------
# PUT /courses/<id> - Update an existing course
# -------------------------------------------
@app.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    # Get the JSON data from the request
    data = request.get_json() or {}
    fields = []
    values = []

    # Build the SET clause dynamically based on provided fields
    if "course_name" in data:
        fields.append("course_name=%s")
        values.append(data["course_name"])
    if "description" in data:
        fields.append("description=%s")
        values.append(data["description"])
    if "credits" in data:
        if not isinstance(data["credits"], int) or data["credits"] <= 0:
            return jsonify({"error": "Credits must be a positive integer"}), 400
        fields.append("credits=%s")
        values.append(data["credits"])

    if not fields:
        return jsonify({"error": "No updatable fields provided"}), 400

    values.append(course_id)

    conn = get_connection()
    cur = conn.cursor()
    # Execute the update query with dynamic fields
    cur.execute(
        f"UPDATE courses SET {', '.join(fields)} WHERE id=%s RETURNING id, course_code, course_name, description, credits",
        tuple(values)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({
        "id": row[0],
        "course_code": row[1],
        "course_name": row[2],
        "description": row[3],
        "credits": row[4]
    }), 200

# -------------------------------------------
# DELETE /courses/<id> - Remove a course
# -------------------------------------------
# Example:
# curl -X DELETE http://localhost:5002/courses/1
@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM courses WHERE id=%s RETURNING id", (course_id,))
    deleted = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
 
    # If no rows were deleted, the course was not found
    if not deleted:
        return jsonify({"error": "Course not found"}), 404

    return jsonify({"message": "Deleted"}), 200

# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)