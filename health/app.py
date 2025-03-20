from flask import Flask, request, jsonify
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Get Database Connection
def get_db_connection():
    """Creates a new database connection"""
    dsn = os.getenv("DATABASE_URL")

    if not dsn:
        raise Exception("DATABASE_URL is not set!")

    # Ensure compatibility with psycopg2
    dsn = dsn.replace("postgresql://", "postgresql+psycopg2://")

    try:
        return psycopg2.connect(dsn)
    except Exception as e:
        raise Exception(f"Database connection error: {str(e)}")

# ➤ REGISTER USER
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        hashed_password = generate_password_hash(password)  # Hash password

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (username, password) VALUES (%s, %s)
        """, (username, hashed_password))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully!"}), 201

    except psycopg2.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ➤ LOGIN USER
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ➤ BOOK APPOINTMENT
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.json
        name = data['name']
        department = data['department']
        doctor = data['doctor']
        date = data['date']
        time = data['time']
        symptoms = data['symptoms']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO appointments (name, department, doctor, date, time, symptoms)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, department, doctor, date, time, symptoms))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Appointment booked successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ➤ GET APPOINTMENTS
@app.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, department, doctor, date, time, symptoms FROM appointments")
        appointments = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"appointments": appointments}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
