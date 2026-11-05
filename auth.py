import bcrypt
import getpass
from customer import is_not_empty, is_valid_phone, is_valid_username, register_customer
from database import get_connection


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

def check_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def get_user_by_username(username):
    conn = None
    cursor = None
    try:
        query = "SELECT CustomerID, FirstName, LastName, Phone, Username, PasswordHash FROM Customers WHERE Username = ?"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        return cursor.fetchone()
    except Exception:
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def login():
    username = input("Username: ").strip()

    password = get_password("Password: ")

    user = get_user_by_username(username)
    if user is None: 
        return "Invalid username or password."

    stored_hash = user.PasswordHash
    if not check_password(password, stored_hash): 
        return "Invalid username or password."

    return f"Login successful. Welcome {user.FirstName}!"

def safe_login():
    try:
        return login()
    except Exception:
        return "Something went wrong. Please try again."
    

def get_password(prompt = "password: "):
    return getpass.getpass(prompt)

def register():

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    if not is_not_empty(first_name) or not is_not_empty(last_name):
        print("First name and last name are requaired.")
        return
    
    phone = input("Phone: ").strip() 
    if not is_valid_phone(phone):
        print("Invalid phone number. It must start with 09 and have 11 digits.")
        return
    
    username = input("Username: ").strip() 
    if not is_valid_username(username):
        print("Invalid username. It must be 3 to 50 characters with no spaces.")
        return

    password = get_password("Password: ")
    if len(password) < 6:
        print("Password must be at least 6 characters.")
        return 

    password_hash = hash_password(password)

    result = register_customer(first_name, last_name, phone, username, password_hash)
    print(result)


