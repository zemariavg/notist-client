from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from mysql.connector import Error
import mysql.connector

# KDF - Key Derivation Function for secure password hashing
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this to a secure key in production
# jwt = JWTManager(app)

db_config = {
    'user': '',
    'password': '',
    'database': '',
}

def get_db_connection():
    """Establish and return a connection to the database."""
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     conn = get_db_connection()
#     if conn:
#         cursor = conn.cursor(dictionary=True)
#         try:
#             # Retrieve the user
#             cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
#             user = cursor.fetchone()
#             if not user or not 
#                 return jsonify({"error": "Invalid username or password"}), 401

#             # Generate access token
#             access_token = create_access_token(identity=username)
#             return jsonify({"access_token": access_token}), 200 # OK
#         finally:
#             cursor.close()
#             conn.close()
#     return jsonify({"error": "Database connection failed"}), 500
    