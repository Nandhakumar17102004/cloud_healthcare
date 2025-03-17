from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get Database URL from environment variables
def get_db_connection():
    """Creates a new database connection"""
    dsn = os.getenv("DATABASE_URL")

    if not dsn:
        raise Exception("DATABASE_URL is not set!")

    # Fix the connection string for compatibility
    dsn = dsn.replace("postgresql://", "postgresql+psycopg2://")

    return psycopg2.connect(dsn)

# ➤ REGISTER USER
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = data['password']  # Ideally, hash this before saving!

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (username, password) VALUES (%s, %s)
        """, (username, password))

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

        cur.execute("""
            SELECT * FROM users WHERE username = %s AND password = %s
        """, (username, password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
