import bcrypt
import getpass
from customer import is_not_empty, is_valid_phone, is_valid_username, register_customer


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")

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


