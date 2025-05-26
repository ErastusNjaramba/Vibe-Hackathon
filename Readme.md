 A web-based tool to automate patient follow-up reminders for clinics using HTML, CSS, JavaScript, Python, and MySQL.

 ## Setup
 1. Install dependencies: `pip install flask mysql-connector-python`
 2. Set up MySQL: Run `database.sql`
 3. Update `app.py` with your MySQL credentials
 4. Run: `python app.py`

 ## Features
 - Add patient appointments via a web form
 - View upcoming appointments in a dashboard
 - Simulate/send reminders via console (Twilio planned)

 ## Future Improvements
 - Twilio SMS/WhatsApp integration
 - Advanced AI for personalized messages
 - Multi-channel support (email, WhatsApp)