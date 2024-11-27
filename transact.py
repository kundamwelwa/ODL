import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import csv

# Define paths
base_dir = 'E:\\KELLY\\PROJECTS\ODL\\Final_Year_Project\\ATM-Security-Face-Recognition-OTP\\Security - Copy (2)\\login-verification-master'
data_file_path = os.path.join(base_dir, 'data.txt')
image_file_path = os.path.join(base_dir, 'images', 'Atm.jpg')
details_csv_path = os.path.join(base_dir, 'Details', 'Details.csv')

def get_user_name(user_id):
    """Retrieve the user's name and balance from the CSV file."""
    try:
        with open(details_csv_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Id"] == user_id:
                    return row["Name"], float(row["deposit_amount"])
        return "User not found", 0
    except FileNotFoundError:
        print(f"File not found: {details_csv_path}")
        return "Error", 0
    except Exception as e:
        print(f"Error reading user data: {e}")
        return "Error", 0

def update_user_details_card(user_name, balance):
    """Update the user details card with the latest balance."""
    global user_details_label, balance_label
    user_details_label.config(text=f"WELCOME: {user_name}")
    balance_label.config(text=f"Balance: {balance:.2f}")

def saving_data(user_id, user_data):
    """Save updated user data to the JSON file."""
    try:
        # Load existing data from JSON file
        if os.path.exists(data_file_path):
            with open(data_file_path, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        else:
            existing_data = {}

        # Update or create entry for the user
        if user_id not in existing_data:
            existing_data[user_id] = {}
        existing_data[user_id] = user_data

        # Save the updated data
        with open(data_file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print(f"File not found: {data_file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {data_file_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

def update_csv(user_id, current_balance):
    """Update user balance in the CSV file."""
    try:
        updated_data = []
        with open(details_csv_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Id"] == user_id:
                    row["deposit_amount"] = str(current_balance)
                updated_data.append(row)
        
        with open(details_csv_path, mode="w", newline="") as file:
            fieldnames = ["Id", "Name", "phone_number", "deposit_amount"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)
    except FileNotFoundError:
        print(f"File not found: {details_csv_path}")
    except Exception as e:
        print(f"Error updating CSV: {e}")

def update_deposit(user_id, deposit_amount):
    """Update balance after deposit and save changes to CSV and JSON files."""
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        if user_id in existing_data:
            user_data = existing_data[user_id]
            current_balance = float(user_data.get("deposit_amount", 0))
            current_balance += deposit_amount
            user_data["deposit_amount"] = current_balance
            saving_data(user_id, user_data)  # Save updated user data
            update_csv(user_id, current_balance)  # Update CSV file
            update_user_details_card(user_data.get("name", "Unknown"), current_balance)  # Update UI
            return f"Deposited {deposit_amount} successfully."
        else:
            return "User not found in data file."
    except FileNotFoundError:
        return f"File not found: {data_file_path}"
    except json.JSONDecodeError:
        return "Error decoding JSON from the file."
    except Exception as e:
        return f"Error updating deposit: {e}"

def update_withdraw(user_id, withdraw_amount):
    """Update balance after withdrawal and save changes to CSV and JSON files."""
    try:
        with open(data_file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)

        if user_id in existing_data:
            user_data = existing_data[user_id]
            current_balance = float(user_data.get("deposit_amount", 0))
            if current_balance >= withdraw_amount:
                current_balance -= withdraw_amount
                user_data["deposit_amount"] = current_balance
                saving_data(user_id, user_data)  # Save updated user data
                update_csv(user_id, current_balance)  # Update CSV file
                update_user_details_card(user_data.get("name", "Unknown"), current_balance)  # Update UI
                return f"Withdrew {withdraw_amount} successfully."
            else:
                return "Insufficient funds."
        else:
            return "User not found in data file."
    except FileNotFoundError:
        return f"File not found: {data_file_path}"
    except json.JSONDecodeError:
        return "Error decoding JSON from the file."
    except Exception as e:
        return f"Error updating withdrawal: {e}"

def open_withdraw_window(user_id):
    """Open the withdrawal window."""
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw")
    withdraw_window.geometry("400x200")

    style = ttk.Style()
    style.configure("TLabel", font=("Poppins", 12), background="#f2f2f2")
    style.configure("TButton", font=("Poppins", 12), padding=10, relief="flat", background="#007bff", foreground="#ffffff")
    style.map("TButton", background=[("active", "#0056b3")], foreground=[("active", "#ffffff")])

    ttk.Label(withdraw_window, text="Enter Withdraw Amount:").pack(pady=10)
    withdraw_entry = ttk.Entry(withdraw_window, font=("Poppins", 16), width=20)
    withdraw_entry.pack(pady=10)

    withdraw_notification = ttk.Label(withdraw_window, text="Notification", background="grey", foreground="white", width=50, anchor="center")
    withdraw_notification.pack(pady=10)

    def perform_withdraw():
        try:
            withdraw_amount = float(withdraw_entry.get())
            message = update_withdraw(user_id, withdraw_amount)
            withdraw_notification.config(text=message)
        except ValueError:
            withdraw_notification.config(text="Invalid amount entered.")
        
        withdraw_window.destroy()

    ttk.Button(withdraw_window, text="Withdraw", command=perform_withdraw).pack(pady=10)

def open_deposit_window(user_id):
    """Open the deposit window."""
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit")
    deposit_window.geometry("400x200")

    style = ttk.Style()
    style.configure("TLabel", font=("Poppins", 12), background="#f2f2f2")
    style.configure("TButton", font=("Poppins", 12), padding=10, relief="flat", background="#28a745", foreground="#ffffff")
    style.map("TButton", background=[("active", "#218838")], foreground=[("active", "#ffffff")])

    ttk.Label(deposit_window, text="Enter Deposit Amount:").pack(pady=10)
    deposit_entry = ttk.Entry(deposit_window, font=("Poppins", 16), width=20)
    deposit_entry.pack(pady=10)

    deposit_notification = ttk.Label(deposit_window, text="Notification", background="grey", foreground="white", width=50, anchor="center")
    deposit_notification.pack(pady=10)

    def perform_deposit():
        try:
            deposit_amount = float(deposit_entry.get())
            message = update_deposit(user_id, deposit_amount)
            deposit_notification.config(text=message)
        except ValueError:
            deposit_notification.config(text="Invalid amount entered.")
        
        deposit_window.destroy()

    ttk.Button(deposit_window, text="Deposit", command=perform_deposit).pack(pady=10)

def check_balance_window(user_id):
    """Open the check balance window."""
    check_window = tk.Toplevel()
    check_window.title("Check Balance")
    check_window.geometry("400x200")

    style = ttk.Style()
    style.configure("TLabel", font=("Poppins", 16), background="#f2f2f2")
    style.configure("TButton", font=("Poppins", 12), padding=10, relief="flat", background="#17a2b8", foreground="#ffffff")
    style.map("TButton", background=[("active", "#117a8b")], foreground=[("active", "#ffffff")])

    user_name, current_balance = get_user_name(user_id)
    ttk.Label(check_window, text=f"HELLO: {user_name}").pack(pady=10)
    ttk.Label(check_window, text=f"Your Balance is: {current_balance:.2f}").pack(pady=10)

    ttk.Button(check_window, text="Close", command=check_window.destroy).pack(pady=10)

def transaction(user_id):
    """Create the main transaction window."""
    window = tk.Toplevel()
    window.title("Transaction Window")
    window.geometry("1200x520+300+100")

    style = ttk.Style()
    style.configure("TLabel", font=("Poppins", 14), background="#f2f2f2")
    style.configure("TButton", font=("Poppins", 14), padding=10, relief="flat", background="#6c757d", foreground="#ffffff")
    style.map("TButton", background=[("active", "#5a6268")], foreground=[("active", "#ffffff")])

    left_frame = tk.Frame(window)
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")

    try:
        image = Image.open(image_file_path)
        image = ImageTk.PhotoImage(image)
        tk.Label(left_frame, image=image).pack()
    except FileNotFoundError:
        print(f"Image file not found: {image_file_path}")

    right_frame = tk.Frame(window)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    user_name, current_balance = get_user_name(user_id)
    global user_details_label, balance_label
    user_details_frame = tk.Frame(right_frame, bg="#f8f9f9", padx=20, pady=10, borderwidth=2, relief="solid")
    user_details_frame.pack(pady=10, fill="x")

    user_details_label = ttk.Label(user_details_frame, text=f"WELCOME: {user_name}", font=("Poppins", 16), background="#f8f9f9")
    user_details_label.pack(pady=5)

    balance_label = ttk.Label(user_details_frame, text=f"Balance: {current_balance:.2f}", font=("Poppins", 16), background="#f8f9f9")
    balance_label.pack(pady=5)

    ttk.Button(right_frame, text="Withdraw", command=lambda: open_withdraw_window(user_id)).pack(pady=10)
    ttk.Button(right_frame, text="Deposit", command=lambda: open_deposit_window(user_id)).pack(pady=10)
    ttk.Button(right_frame, text="Check Balance", command=lambda: check_balance_window(user_id)).pack(pady=10)
    ttk.Button(right_frame, text="Logout", command=window.destroy).pack(pady=10)

    window.mainloop()

