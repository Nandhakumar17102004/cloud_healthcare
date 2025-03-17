from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Get Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Creates a new database connection"""
    return psycopg2.connect(DATABASE_URL)

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
