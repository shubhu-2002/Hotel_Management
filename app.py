from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Create the 'rooms' table
        cursor.execute('''CREATE TABLE IF NOT EXISTS rooms(
            id INTEGER PRIMARY KEY, room_number TEXT UNIQUE, type TEXT, price INTEGER, status TEXT)''')
        # Create the 'bookings' table
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY, room_id INTEGER, customer_name TEXT, checkin_date TEXT, checkout_date TEXT)''')
        conn.commit()

init_db()

def update_room_numbers():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        
       
        cursor.execute("SELECT id FROM rooms ORDER BY id")
        rooms = cursor.fetchall()
        
        
        new_room_number = 101
        for room in rooms:
            cursor.execute("UPDATE rooms SET room_number = ? WHERE id = ?", (str(new_room_number), room[0]))
            new_room_number += 1
            if new_room_number > 510: 
                break
        
        conn.commit()

    print("Room numbers updated successfully!")


update_room_numbers()


# Login Route
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

# Home Page
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

# View Rooms
@app.route('/rooms')
def rooms():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, room_number, type, price, status FROM rooms ORDER BY room_number")
        rooms = cursor.fetchall()
    return render_template('rooms.html', rooms=rooms)

# Book a Room
@app.route('/book_room', methods=['GET', 'POST'])
def book_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        customer_name = request.form['customer_name']
        checkin_date = request.form['checkin_date']
        checkout_date = request.form['checkout_date']

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT status FROM rooms WHERE id = ?", (room_id,))
            room_status = cursor.fetchone()

            if room_status and room_status[0] == 'BOOKED':
                
                return render_template('booking.html', error=f"Room {room_id} is already booked.")

            # Book the room
            cursor.execute("INSERT INTO bookings (room_id, customer_name, checkin_date, checkout_date) VALUES (?, ?, ?, ?)",
                           (room_id, customer_name, checkin_date, checkout_date))
            cursor.execute("UPDATE rooms SET status = 'BOOKED' WHERE id = ?", (room_id,))
            conn.commit()

        return redirect(url_for('customers'))
    else:
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, room_number FROM rooms WHERE status = 'AVAILABLE'")
            available_rooms = cursor.fetchall()
        return render_template('booking.html', available_rooms=available_rooms)


# View Bookings
@app.route('/customers')
def customers():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        customers = cursor.fetchall()
    return render_template('customer.html', customers=customers)

# Delete Booking
@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT room_id FROM bookings WHERE id = ?", (booking_id,))
        room_id = cursor.fetchone()
        
        if room_id:
            room_id = room_id[0] 
            cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
            cursor.execute("UPDATE rooms SET status = 'AVAILABLE' WHERE id = ?", (room_id,))
            conn.commit()
    return redirect(url_for('customers'))

if __name__ == '__main__':
    app.run(debug=True)
