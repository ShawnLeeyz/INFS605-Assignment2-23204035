"""
This module contains the main application logic for the notification service.
It contains the logic to send a notification when a feedback is submitted, 
and also contains the logic to get all the notifications in the notificaiton db.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS          
import psycopg2                    
import os
import json
import time

app = Flask(__name__)
CORS(app)  # permit Cross-Origin requests from the frontend during development


# DATABASE_URL read from environment so we can change DB location without changing code.
# Default value is useful for Docker Compose; in production put a secure value in env.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://notificationuser:notificationpass@notification-db:5432/notificationdb"
)

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
        "Hello from notification service (with Postgres DB)! "
        "This is a line of text to let you know that the API service is running smoothly"
    )

# -----------------------------
# POST /notification - Send a notification
# -----------------------------
@app.route("/notification", methods=["POST"])
def send_notification():

    #Getting the data from the request
    data = request.get_json() or {}
    student_id = data.get("student_id")
    message = data.get("message")

    # Check if the required fields are entered
    if not all([student_id, message]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO notifications (student_id, message) VALUES (%s, %s) RETURNING id", (student_id, message))
    notification_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Notification sent successfully", "notification_id": notification_id}), 201

# -----------------------------
# GET /notification - Retrieve notifications
# -----------------------------
@app.route("/notification", methods=["GET"])
def get_notifications():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM notifications")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    notifications = [{"id": row[0], "student_id": row[1], "message": row[2], "sent_at": row[3]} for row in rows]
    return jsonify(notifications), 200

# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)

