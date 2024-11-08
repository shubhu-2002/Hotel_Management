#Hotel Management System

A Hotel Management System built with Flask and SQLite to manage room bookings, customer information, and availability of rooms.

#Table of Contents:

Project Overview
Features
Technologies Used
Installation
Usage

#Project Overview
This project is a web-based Hotel Management System that allows hotel staff to manage room bookings, check room availability, and handle customer information. It's a simple yet functional system created for learning purposes and to demonstrate the basic workings of a hotel booking platform.

#Features
User Authentication: Simple login system for admin users.
Room Management: View available rooms, update room status, and manage room information.
Booking Management: Book rooms for customers, set check-in/check-out dates.
Customer Management: View and manage customer details for booked rooms.

#Technologies Used
Frontend: HTML, CSS
Backend: Python (Flask)
Database: SQLite
Other Tools: Git for version control

#Installation
Clone the repository:

bash
Copy code
git clone https://github.com/shubhu-2002/Hotel_Management.git
cd Hotel_Management
Set up a virtual environment (optional but recommended):

bash
Copy code
python -m venv env
.\env\Scripts\activate.ps1

Initialize the database: Make sure the init_db() function in app.py is called to create the required tables in database.db.

Run the application:

bash
Copy code
python app.py
Access the application: Open your browser and go to http://127.0.0.1:5000.

Usage
Login: Use the default credentials:

Username: admin
Password: password
Home Page: View options for room management, booking rooms, and viewing customer information.

Room Management: View all rooms, check availability, and update room information.

Booking: Book a room for a customer, selecting check-in and check-out dates.

Customer Management: View and manage customer details for each booking.
