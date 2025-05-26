from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime, timedelta
import time
import threading

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="Nakara",  # Replace with your MySQL password
    database="healthtech"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_name = request.form['patient_name']
    phone = request.form['phone']
    appointment_time = request.form['appointment_time']
    
    query = "INSERT INTO appointments (patient_name, phone, appointment_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (patient_name, phone, appointment_time))
    db.commit()
    return render_template('index.html', message="Appointment added!")

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    return render_template('dashboard.html', appointments=appointments)

def send_reminders():
    while True:
        now = datetime.now()
        reminder_time = now + timedelta(minutes=30)
        query = "SELECT * FROM appointments WHERE appointment_time <= %s AND reminder_sent = FALSE"
        cursor.execute(query, (reminder_time,))
        due_appointments = cursor.fetchall()
        
        for appt in due_appointments:
            print(f"Sending reminder to {appt[2]}: Hi {appt[1]}, your appointment is at {appt[3]}")
            cursor.execute("UPDATE appointments SET reminder_sent = TRUE WHERE id = %s", (appt[0],))
            db.commit()
        time.sleep(60)

if __name__ == '__main__':
    threading.Thread(target=send_reminders, daemon=True).start()
    app.run(debug=True)