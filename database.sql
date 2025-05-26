CREATE DATABASE healthtech;
     USE healthtech;
     CREATE TABLE appointments (
         id INT AUTO_INCREMENT PRIMARY KEY,
         patient_name VARCHAR(100),
         phone VARCHAR(15),
         appointment_time DATETIME,
         reminder_sent BOOLEAN DEFAULT FALSE
     );
