from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime, timedelta
import time
import threading
from twilio.rest import Client

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

# Add Twilio credentials
account_sid = 'your_account_sid'  # From Twilio dashboard
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

def send_reminders():
    while True:
        now = datetime.now()
        reminder_time = now + timedelta(minutes=30)
        query = "SELECT * FROM appointments WHERE appointment_time <= %s AND reminder_sent = FALSE"
        cursor.execute(query, (reminder_time,))
        due_appointments = cursor.fetchall()
        
        for appt in due_appointments:
            message = f"Hi {appt[1]}, your appointment is at {appt[3].strftime('%Y-%m-%d %H:%M')}"
            client.messages.create(
                body=message,
                from_='your_twilio_number',
                to=appt[2]
            )
            print(f"Sending SMS to {appt[2]}: {message}")
            cursor.execute("UPDATE appointments SET reminder_sent = TRUE WHERE id = %s", (appt[0],))
            db.commit()
        time.sleep(60)

import random

def generate_reminder_message(patient_name, appointment_time):
    templates = [
        f"Hi {patient_name}, don't forget your appointment on {appointment_time.strftime('%Y-%m-%d %H:%M')}!",
        f"Hello {patient_name}, we're looking forward to seeing you at {appointment_time.strftime('%Y-%m-%d %H:%M')}.",
        f"Reminder: {patient_name}, your visit is scheduled for {appointment_time.strftime('%Y-%m-%d %H:%M')}."
    ]
    return random.choice(templates)

# Update send_reminders function
def send_reminders():
    while True:
        now = datetime.now()
        reminder_time = now + timedelta(minutes=30)
        query = "SELECT * FROM appointments WHERE appointment_time <= %s AND reminder_sent = FALSE"
        cursor.execute(query, (reminder_time,))
        due_appointments = cursor.fetchall()
        
        for appt in due_appointments:
            message = generate_reminder_message(appt[1], appt[3])
            print(f"Sending reminder to {appt[2]}: {message}")  # Replace with Twilio if set up
            cursor.execute("UPDATE appointments SET reminder_sent = TRUE WHERE id = %s", (appt[0],))
            db.commit()
        time.sleep(60)
        
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_name = request.form['patient_name'].strip()
    phone = request.form['phone'].strip()
    appointment_time = request.form['appointment_time']
    if not (patient_name and phone and appointment_time):
        return render_template('index.html', message="All fields are required!")
    query = "INSERT INTO appointments (patient_name, phone, appointment_time) VALUES (%s, %s, %s)"
    cursor.execute(query, (patient_name, phone, appointment_time))
    db.commit()
    return render_template('index.html', message="Appointment added!")