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

def get_all_customers():
    conn = None
    cursor = None 
    try:
        query = "SELECT CustomerID, FirstName, LastName, Phone, Username, CreatedAt FROM Customers"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        customers = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not customers:
            print("No customers found.")
            return

        print(f"{'ID':<5} | {'FirstName':<12} | {'LastName':<12} | {'Phone':<12} | {'Username':<15} | {'CreatedAt':<20}")
        print("-" * 85)
        for customer in customers:
            print(f"{customer['CustomerID']:<5} | {customer['FirstName']:<12} | {customer['LastName']:<12} | {customer['Phone']:<12} | {customer['Username']:<15} | {str(customer['CreatedAt']):<20}")
    except Exception as e:
        print("Failed to fetch customers.")
    finally: 
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def search_customers(search_type, term):
    conn = None 
    cursor = None 
    try: 
        conn = get_connection() 
        cursor = conn.cursor()
        columns_map = {
            "1": "FirstName",
            "2": "LastName",
            "3": "Phone"
        }
        column = columns_map.get(search_type)
        if column is None:
            print("Invalid search type.") 
            return

        query = f"SELECT CustomerID, FirstName, LastName, Phone, Username, CreatedAt FROM Customers WHERE {column} LIKE ?"
        like_value = f"%{term}%" 
        cursor.execute(query, (like_value,))
        columns = [col[0] for col in cursor.description]
        customers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if not customers:
            print("No customers found.")
            return
        print(f"{'ID':<5} | {'FirstName':<12} | {'LastName':<12} | {'Phone':<12} | {'Username':<15} | {'CreatedAt':<20}")
        print("-" * 85)
        for customer in customers:
            print(f"{customer['CustomerID']:<5} | {customer['FirstName']:<12} | {customer['LastName']:<12} | {customer['Phone']:<12} | {customer['Username']:<15} | {str(customer['CreatedAt']):<20}")

    except Exception:
        print("Failed to search customers.")  
        
    finally:
        if cursor is not None: 
            cursor.close() 
        if conn is not None: 
            conn.close()


def search_customer_menu():
    print("=================================")
    print("      Search Customer")
    print("=================================")
    print("1. Search by First Name")
    print("2. Search by Last Name")
    print("3. Search by Phone")
    print("4. Back")

    choice = input("choose: ").strip()
    if choice == "4":
        return
    term = input("Enter search term: ").strip()
    if not term:
        print("Search term cannot be empty.")
        return

    search_customers(choice, term)


def get_customer_by_id(customer_id):
    conn = None 
    cursor = None 
    try: 
        query = "SELECT CustomerID, FirstName, LastName, Phone, Username, CreatedAt FROM Customers WHERE CustomerID = ?"
        conn = get_connection() 
        cursor = conn.cursor()
        cursor.execute(query, (customer_id,))
        return cursor.fetchone()
    except Exception :
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close() 
    

def update_customer(customer_id, first_name, last_name, phone):
    conn = None
    cursor = None
    try:
        query = "UPDATE Customers SET FirstName = ?, LastName = ?, Phone = ? WHERE CustomerID = ?"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, phone, customer_id))
        if cursor.rowcount == 0:
            conn.rollback()
            return "Customer not found."
        conn.commit()
        return "Customer updated successfully."
    except Exception:
        if conn is not None:
            conn.rollback()
        return "Update failed. Please try again."
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def update_customer_menu():
    try:
        customer_id = int(input("Customer ID: ").strip())
        customer = get_customer_by_id(customer_id) 
        if customer is None: 
            print("Customer not found.")
            return
        print(f"Current First Name: {customer.FirstName}")
        print(f"Current Last Name: {customer.LastName}")
        print(f"Current Phone: {customer.Phone}")

        new_first_name = input("New First Name (leave empty to keep): ").strip()
        if not new_first_name:
            new_first_name = customer.FirstName

        new_last_name = input("New Last Name (leave empty to keep): ").strip()
        if not new_last_name:
            new_last_name = customer.LastName

        new_phone = input("New Phone (leave empty to keep): ").strip()
        if not new_phone:
            new_phone = customer.Phone

        if not is_not_empty(new_first_name) or not is_not_empty(new_last_name):
            print("First name and last name are required.")
            return

        if not is_valid_phone(new_phone):
            print("Invalid phone number. It must start with 09 and have 11 digits.")
            return
        result = update_customer(customer_id, new_first_name, new_last_name, new_phone)
        print(result)
    except ValueError:
        print("Customer ID must be a number.")
    except Exception as e:
        print("Something went wrong. Please try again.")
        print("DEBUG:", repr(e))

