import mysql.connector as mq
from tabulate import tabulate
import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_database():
    try:
        con = mq.connect(host=os.getenv('host'), user=os.getenv('user'), password=os.getenv('password'), database=os.getenv('database'))
        return con
    except mq.Error as err:
        print("Error connecting to database:", err)
        return None

def menu():
    print("\n\t\t\t\tRESTAURANT MANAGEMENT SYSTEM\n\n")
    print("\t\t\t\t\tMAIN MENU\n")
    print("\t\t1. Make Reservation\t\t 2. View Reservations\n\n\t\t3. Cancel Reservation\t\t 4. Add Menu Item\n")
    print("\t\t5. View Menu\t\t\t 6. Place Order\n")
    print("\t\t7. Add Staff Present\t\t 8. Exit")

def make_reservation():
    print("\n\t\t\t\tMAKE RESERVATION")
    name = input("Enter Your Name: ")
    guests = int(input("Enter Number of Guests: "))
    date_time = input("Enter Date and Time (YYYY-MM-DD HH:MM): ")

    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "INSERT INTO reservations (name, guests, date_time) VALUES (%s, %s, %s)"
        data = (name, guests, date_time)
        cur.execute(query, data)
        con.commit()
        print("\nReservation confirmed.")
    except mq.Error as err:
        print("Error making reservation:", err)
    finally:
        con.close()

def view_reservations():
    print("\n\t\t\t\tVIEW RESERVATIONS")
    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "SELECT reservation_id, name, date_time FROM reservations"
        cur.execute(query)
        res = cur.fetchall()
        if res:
            print(tabulate(res, headers=["Reservation ID", "Name", "Date Time"]))
        else:
            print("No reservations found.")
    except mq.Error as err:
        print("Error viewing reservations:", err)
    finally:
        con.close()

def cancel_reservation():
    print("\n\t\t\t\tCANCEL RESERVATION")
    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "SELECT reservation_id, name, date_time FROM reservations"
        cur.execute(query)
        res = cur.fetchall()
        if res:
            print(tabulate(res, headers=["Reservation ID", "Name", "Date Time"]))
            reservation_id = int(input("Enter the Reservation ID to Cancel: "))
            cur.execute("DELETE FROM reservations WHERE reservation_id = %s", (reservation_id,))
            con.commit()
            print("Reservation with ID", reservation_id, "has been canceled.")
        else:
            print("No reservations found.")
    except mq.Error as err:
        print("Error canceling reservation:", err)
    finally:
        con.close()

def add_menu_item():
    print("\n\t\t\t\tADD MENU ITEM")
    item_name = input("Enter Menu Item Name: ")
    price = float(input("Enter Price: "))

    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "INSERT INTO menu (item_name, price) VALUES (%s, %s)"
        data = (item_name, price)
        cur.execute(query, data)
        con.commit()
        print("\nMenu item added successfully.")
    except mq.Error as err:
        print("Error adding menu item:", err)
    finally:
        con.close()

def view_menu():
    print("\n\t\t\t\tVIEW MENU")
    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "SELECT * FROM menu"
        cur.execute(query)
        res = cur.fetchall()
        if res:
            print(tabulate(res, headers=["ID","Menu Item Name", "Price"]))
        else:
            print("No menu items found.")
    except mq.Error as err:
        print("Error viewing menu:", err)
    finally:
        con.close()

def place_order():
    print("\n\t\t\t\tPLACE ORDER")

    order_type = int(input("Type of Order\n1-DineIn \n2-Takeaway\n3-Delivery:\n "))

    if order_type == 1:
        customer_name = input("Enter Customer Name: ")
        view_menu()
        item_ids = [int(item_id.strip()) for item_id in input("Enter Menu Item IDs (comma separated): ").split(",")]
        table_number = input("Enter Table Number: ")

        total_amount = sum([get_menu_item_price_by_id(item_id) for item_id in item_ids])

        print("\nCustomer", customer_name, "seated at Table", table_number)
        print("Total Amount to Pay: ₹", total_amount)

    elif order_type == 3:
        customer_name = input("Enter Customer Name: ")
        phone_number = input("Enter Phone Number: ")
        location = input("Enter Delivery Location: ")
        view_menu()
        item_ids = [int(item_id.strip()) for item_id in input("Enter Menu Item IDs (comma separated): ").split(",")]
        total_amount = sum([get_menu_item_price_by_id(item_id) for item_id in item_ids])

        print("\nDelivery order for customer", customer_name, "confirmed.")
        print("Total Amount to Pay: ₹", total_amount)

    elif order_type == 2:
        customer_name = input("Enter Customer Name: ")
        phone_number = input("Enter Phone Number: ")
        pick_up_time = input("Enter Pick Up Time (HH:MM): ")
        view_menu()
        item_ids = [int(item_id.strip()) for item_id in input("Enter Menu Item IDs (comma separated): ").split(",")]
        total_amount = sum([get_menu_item_price_by_id(item_id) for item_id in item_ids])

        print("\nTakeaway order for customer", customer_name, "confirmed.")
        print("Total Amount to Pay: ₹", total_amount)
        print("Will be picked up at", pick_up_time)

    else:
        print("Invalid order type.")

def get_menu_item_price_by_id(item_id):
    con = connect_to_database()
    if con is None:
        return None

    try:
        cur = con.cursor()
        query = "SELECT price FROM menu WHERE Id = %s"
        cur.execute(query, (item_id,))
        price = cur.fetchone()[0]
        return price
    except mq.Error as err:
        print("Error getting menu item price:", err)
        return None
    finally:
        con.close()

def add_staff_present():
    print("\n\t\t\t\tADD STAFF PRESENT")
    staff_name = input("Enter Staff Name: ")

    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        query = "INSERT INTO staff (staff_name) VALUES (%s)"
        data = (staff_name,)
        cur.execute(query, data)
        con.commit()
        print("\nStaff added successfully.")
    except mq.Error as err:
        print("Error adding staff:", err)
    finally:
        con.close()

def main():
    # Connect to MySQL and set up database tables
    con = connect_to_database()
    if con is None:
        return

    try:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS reservations (reservation_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, guests INT NOT NULL, date_time DATETIME NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS menu (Id INT AUTO_INCREMENT PRIMARY KEY,item_name VARCHAR(30), price DECIMAL(10, 2) NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS staff (staff_id INT AUTO_INCREMENT PRIMARY KEY, staff_name VARCHAR(255) NOT NULL)")
        con.commit()
    except mq.Error as err:
        print("Error creating tables:", err)
    finally:
        con.close()

if __name__ == "__main__":
    main()

while True:
    menu()
    ch = int(input("Enter your choice (1-8): "))
    if ch == 1:
        make_reservation()
    elif ch == 2:
        view_reservations()
    elif ch == 3:
        cancel_reservation()
    elif ch == 4:
        add_menu_item()
    elif ch == 5:
        view_menu()
    elif ch == 6:
        place_order()
    elif ch == 7:
        add_staff_present()
    elif ch == 8:
        exit()
    else:
        print("Invalid choice. Please choose a number from 1 to 8.")

    ch = int(input("\nPress 0 to continue, any other number to exit: "))
    if ch != 0:
        break
