from auth import register, safe_login
from customer import (
    get_all_customers, 
    search_customer_menu, 
    update_customer_menu, 
    delete_customer_menu,
)


def show_main_menu():
    print("\n=================================")
    print("   Store Customer Management")
    print("=================================")
    print("1. Register Customer")
    print("2. Login")
    print("3. Exit")


def show_customer_menu():
    print("\n=================================")
    print("        Customer Menu")
    print("=================================")
    print("1. Show Customers")
    print("2. Search Customer")
    print("3. Update Customer")
    print("4. Delete Customer")
    print("5. Logout")

def customer_menu():
    while True: 
        show_customer_menu()
        choice = input("Choose: ").strip()
        if choice == "1": 
            get_all_customers() 
        elif choice == "2": 
            search_customer_menu()
        elif choice == "3" : 
            update_customer_menu( )
        elif choice == "4": 
            delete_customer_menu() 
        elif choice == "5": 
            print("Logged out successfully.")
            break 
        else: 
            print("Invalid choice.") 


def main_menu(): 
    while True: 
        show_main_menu() 
        choice = input("Choose: ").strip() 
        if choice == "1":
            register()
        elif choice == "2":
            result = safe_login()
            print(result)
            if "Login successful" in result:
                    customer_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")