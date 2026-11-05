from datetime import datetime
from database import get_connection


def is_not_empty(value):
    return value.strip() != ""


def is_valid_phone(phone):
    return phone.startswith("09") and len(phone) == 11 and phone.isdigit()

def is_valid_username(username):
    return is_not_empty(username) and " " not in username and 3 <= len(username) <= 50


def register_customer(first_name, last_name, phone, username, password_hash):
    conn = None
    cursor = None
    try:
        query = "INSERT INTO Customers (FirstName, LastName, Phone, Username, PasswordHash, CreatedAt) VALUES (?, ?, ?, ?, ?, ?)"
        created_at = datetime.now()
        values = (first_name, last_name, phone, username, password_hash, created_at)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        return "Customer registered successfully."
    except Exception as e:
        if conn is not None:
            conn.rollback()
        if "UNIQUE" in str(e) or "duplicate" in str(e).lower():
            return "This username already exists."
        return "Registration failed. Please try again."
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
