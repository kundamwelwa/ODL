import os
import tkinter as tk
import base64
from PIL import Image, ImageTk
import json
import csv
import bcrypt
from transact import transaction
from otp import otp_verification

# Base directory for all file paths
base_dir = r'E:\KELLY\PROJECTS\ODL\Final_Year_Project\ATM-Security-Face-Recognition-OTP\Security - Copy (2)\login-verification-master'

# Define paths to files
data_file_path = os.path.join(base_dir, 'data.txt')
image_file_path = os.path.join(base_dir, 'images', 'Atm.jpg')
details_csv_path = os.path.join(base_dir, 'Details', 'Details.csv')

def loading_data():
    """Load user data from a JSON file."""
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extracting nested user data
        processed_data = {}
        for user_id, user_info in data.items():
            if isinstance(user_info, dict) and user_id in user_info:
                user_data = user_info[user_id]
                processed_data[user_id] = user_data

        return processed_data
    except FileNotFoundError:
        print(f"File not found: {data_file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {data_file_path}")
        return {}

def saving_data(data):
    """Save user data to a JSON file."""
    try:
        # Convert to the expected nested structure
        nested_data = {}
        for user_id, user_info in data.items():
            nested_data[user_id] = {user_id: user_info}
            # Also add any additional required information at the same level if necessary
            if 'deposit_amount' in user_info:
                nested_data[user_id]['deposit_amount'] = user_info['deposit_amount']

        with open(data_file_path, 'w', encoding='utf-8') as file:
            json.dump(nested_data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def saving_to_csv(user_data):
    """Append user data to a CSV file."""
    with open(details_csv_path, mode="a", newline="") as file:  # Append mode
        fieldnames = ["Id", "Name", "phone_number", "deposit_amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write to CSV
        writer.writerow({
            "Id": user_data["username"],
            "Name": user_data["name"],
            "phone_number": user_data["phone_number"],
            "deposit_amount": user_data["deposit_amount"]
        })

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_password, provided_password):
    """Check a password against the hashed version."""
    # Decode the base64-encoded password string to bytes
    stored_password_bytes = base64.b64decode(stored_password)
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_bytes)

def update_message(label, text):
    """Update a label's text."""
    label.config(text=text)

def clear_fields(*fields):
    """Clear multiple entry fields."""
    for field in fields:
        field.delete(0, 'end')

def create_login_window():
    """Create the login window."""
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("1200x520+300+100")

    left_frame = tk.Frame(login_window)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    try:
        image = Image.open(image_file_path)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.pack()
    except FileNotFoundError:
        print(f"Image file not found: {image_file_path}")
        return

    right_frame = tk.Frame(login_window)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tk.Label(right_frame, text="LOGIN TO ACCESS YOUR ACCOUNT", font=("Poppins", 24), fg="black").pack(padx=10, pady=(20, 10))

    # Username and password entry fields
    tk.Label(right_frame, text="Card Number:").pack()
    txt = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    txt.pack()

    tk.Label(right_frame, text="Pin:").pack()
    txt2 = tk.Entry(right_frame, font=("Poppins", 16), width=40, show="*")
    txt2.pack()

    login_message = tk.Label(right_frame, text="", bg="Grey", fg="white", width=30, height=1, font=('times', 15, 'bold'))
    login_message.pack(pady=10)

    def track_images(user_id):
        """Proceed to OTP verification."""
        update_message(login_message, "Proceeding to OTP verification")
        otp_verification(user_id, data)

    def login_submit():
        """Handle login submission."""
        username = txt.get()
        password = txt2.get()

        if username in data:
            user_data = data[username]
            if check_password(user_data["password"], password):
                track_images(username)
            else:
                update_message(login_message, "Card Number and PIN do not match")
        else:
            update_message(login_message, "Entered Card Number does not exist")

        clear_fields(txt, txt2)

    tk.Button(right_frame, text="Login", width=15, height=2, font=("Poppins", 16), bg="green", command=login_submit).pack(pady=(20, 10))
    tk.Button(right_frame, text="Cancel", width=15, height=2, font=("Poppins", 16), bg="gray", command=login_window.destroy).pack(pady=(0, 10))

def register():
    """Create the registration window."""
    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.geometry("1200x520+300+100")

    left_frame = tk.Frame(registration_window)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    try:
        image = Image.open(image_file_path)
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.pack()
    except FileNotFoundError:
        print(f"Image file not found: {image_file_path}")
        return

    right_frame = tk.Frame(registration_window)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tk.Label(right_frame, text="Enter your details below to register Your Account", font=("Poppins", 24), fg="dark blue").pack(padx=10, pady=(20, 10))

    # Registration entry fields
    tk.Label(right_frame, text="Name:").pack()
    name_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    name_entry.pack()

    tk.Label(right_frame, text="Mobile Number:").pack()
    mobile_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    mobile_entry.pack()

    tk.Label(right_frame, text="Account Number:").pack()
    account_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    account_entry.pack()

    tk.Label(right_frame, text="Deposit Amount:").pack()
    deposit_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    deposit_entry.pack()

    tk.Label(right_frame, text="Card Number:").pack()
    card_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40)
    card_entry.pack()

    tk.Label(right_frame, text="Pin:").pack()
    pin_entry = tk.Entry(right_frame, font=("Poppins", 16), width=40, show="*")
    pin_entry.pack()

    register_message = tk.Label(right_frame, text="", bg="Grey", fg="white", width=30, height=1, font=('times', 15, 'bold'))
    register_message.pack(pady=10)

    def register_user():
        """Register a new user."""
        username = card_entry.get()
        name = name_entry.get()
        phone_number = mobile_entry.get()
        deposit_amount = deposit_entry.get()
        account_number = account_entry.get()
        password = pin_entry.get()

        if username in data:
            update_message(register_message, "Account Number already exists")
        else:
            hashed_password = base64.b64encode(hash_password(password)).decode('utf-8')
            user_data = {
                "username": username,
                "name": name,
                "phone_number": phone_number,
                "deposit_amount": deposit_amount,
                "account_number": account_number,
                "password": hashed_password
            }

            data[username] = user_data
            saving_data(data)
            saving_to_csv(user_data)
            update_message(register_message, "Registered successfully!")

        clear_fields(name_entry, mobile_entry, account_entry, deposit_entry, card_entry, pin_entry)

    tk.Button(right_frame, text="Register", width=15, height=2, font=("Poppins", 16), bg="green", command=register_user).pack(pady=(20, 10))
    tk.Button(right_frame, text="Cancel", width=15, height=2, font=("Poppins", 16), bg="gray", command=registration_window.destroy).pack(pady=(0, 10))

# Main Application Window
root = tk.Tk()
root.title("ZUT ATM SYSTEM")
root.geometry("800x400+300+200")

tk.Label(root, text="WELCOME TO ZUT ATM SYSTEM", font=("Poppins", 24), fg="black").pack(pady=20)

tk.Button(root, text="Login", width=15, height=2, font=("Poppins", 16), bg="green", command=create_login_window).pack(pady=(0, 10))
tk.Button(root, text="Register", width=15, height=2, font=("Poppins", 16), bg="blue", command=register).pack(pady=(0, 10))
tk.Button(root, text="Exit", width=15, height=2, font=("Poppins", 16), bg="red", command=root.quit).pack(pady=(0, 10))

# Load data on startup
data = loading_data()

root.mainloop()
