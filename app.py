from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rooms(
            id INTEGER PRIMARY KEY, room_number TEXT, type TEXT, price INTEGER, status TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY, room_id INTEGER, customer_name TEXT, checkin_date TEXT, checkout_date TEXT)''')
        conn.commit()

init_db()

def add_sample_data():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rooms")
        room_count = cursor.fetchone()[0]
        
        if room_count == 0:  
            sample_rooms = [
                ('101', 'Single', 100, 'AVAILABLE'),
                ('102', 'Double', 200, 'AVAILABLE'),
                ('103', 'Suite', 300, 'AVAILABLE')
            ]
            cursor.executemany("INSERT INTO rooms (room_number, type, price, status) VALUES (?, ?, ?, ?)", sample_rooms)
            conn.commit()

add_sample_data()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/rooms')
def rooms():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
    return render_template('rooms.html', rooms=rooms)

@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        customer_name = request.form['customer_name']
        checkin_date = request.form['checkin_date']
        checkout_date = request.form['checkout_date']
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bookings (room_id, customer_name, checkin_date, checkout_date) VALUES (?, ?, ?, ?)",
                           (room_id, customer_name, checkin_date, checkout_date))
            cursor.execute("UPDATE rooms SET status = 'BOOKED' WHERE id = ?", (room_id,))
            conn.commit()
        
        return redirect(url_for('customers'))
    return render_template('booking.html')

@app.route('/customers')
def customers():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        customers = cursor.fetchall()
    return render_template('customer.html', customers=customers)

@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        cursor.execute("UPDATE rooms SET status = 'AVAILABLE' WHERE id = (SELECT room_id FROM bookings WHERE id = ?)", (booking_id,))
        conn.commit()
    return redirect(url_for('customers'))

if __name__ == '__main__':
    app.run(debug=True)
