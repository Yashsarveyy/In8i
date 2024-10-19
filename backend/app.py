from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='registration_db'
        )
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")  # Log the specific error
        return None


# CREATE
@app.route('/register', methods=['POST'])
def create_registration():
    data = request.json
    required_fields = ['name', 'email', 'dob', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields in request'}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Registration (Name, Email, DateOfBirth, PhoneNumber) 
            VALUES (%s, %s, %s, %s)
        """, (data['name'], data['email'], data['dob'], data['phone']))
        conn.commit()
        return jsonify({'message': 'Registration created successfully!'}), 201
    except Error as e:
        return jsonify({'message': f'Error occurred: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

# READ
@app.route('/registrations', methods=['GET'])
def get_registrations():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed'}), 500
    
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Registration")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows), 200

# UPDATE
@app.route('/register/<int:id>', methods=['PUT'])
def update_registration(id):
    data = request.json
    required_fields = ['name', 'email', 'dob', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields in request'}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Registration 
            SET Name = %s, Email = %s, DateOfBirth = %s, PhoneNumber = %s 
            WHERE ID = %s
        """, (data['name'], data['email'], data['dob'], data['phone'], id))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Registration not found'}), 404
        conn.commit()
        return jsonify({'message': 'Registration updated successfully!'}), 200
    except Error as e:
        return jsonify({'message': f'Error occurred: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

# DELETE
@app.route('/register/<int:id>', methods=['DELETE'])
def delete_registration(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection failed'}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Registration WHERE ID = %s", (id,))
        if cursor.rowcount == 0:
            return jsonify({'message': 'Registration not found'}), 404
        conn.commit()
        return jsonify({'message': 'Registration deleted successfully!'}), 200
    except Error as e:
        return jsonify({'message': f'Error occurred: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
