import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from twilio.rest import Client
import os
import csv
from transact import transaction

# Fetch Twilio credentials from environment variables or set them here directly
account_sid = Add the credentials from your Twilio account
auth_token = Add the credentials from your Twilio account
verify_sid = Add the credentials from your Twilio account

otp_entry = None
otp_trials = 0
otp_window = None
user_id = None
user_data = None
verified_number = None
details_csv_path = r'E:\KELLY\PROJECTS\ODL\Final_Year_Project\ATM-Security-Face-Recognition-OTP\Security - Copy (2)\login-verification-master\Details\Details.csv'

def get_twilio_client():
    """Initialize and return a Twilio client."""
    return Client(account_sid, auth_token)

def otp_verification(user_id_param, user_data_param):
    global otp_trials, otp_window, otp_entry, verified_number, user_id, user_data
    user_id = user_id_param
    user_data = user_data_param
    otp_trials = 0
    
    # Send OTP before creating the verification window
    send_otp(user_id)
    
    otp_window = tk.Toplevel()
    otp_window.title("OTP Verification")
    otp_window.geometry("1200x520+300+100")  # Adjust the window size as needed

    # Load and display the image
    try:
        atm_image = Image.open(r"E:\KELLY\PROJECTS\ODL\Final_Year_Project\ATM-Security-Face-Recognition-OTP\Security - Copy (2)\login-verification-master\images\Atm.jpg")
        atm_image = atm_image.resize((480, 480), Image.LANCZOS)
        atm_photo = ImageTk.PhotoImage(atm_image)
        image_label = tk.Label(otp_window, image=atm_photo)
        image_label.image = atm_photo
        image_label.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
    except FileNotFoundError:
        messagebox.showerror("Error", "Image file not found.")
        return

    # Right side (OTP functionality)
    otp_label = tk.Label(otp_window, text="Enter OTP:", font=("Helvetica", 16))
    otp_label.grid(row=0, column=1, pady=10, sticky="e")

    otp_entry = tk.Entry(otp_window, font=("Helvetica", 16), width=20)
    otp_entry.grid(row=0, column=2, pady=10)

    verify_button = tk.Button(otp_window, text="Verify OTP", width=15, height=2, font=("Helvetica", 16), bg="green", command=verify_otp)
    verify_button.grid(row=1, column=2, pady=10)

    # Countdown Label
    global countdown_label, resend_button
    countdown_label = tk.Label(otp_window, text="00:30", font=("Helvetica", 16), fg="red")
    countdown_label.grid(row=1, column=1, pady=10)

    # Resend OTP Button (Initially hidden)
    resend_button = tk.Button(otp_window, text="Resend OTP", width=15, height=2, font=("Helvetica", 16), bg="blue", command=resend_otp)
    resend_button.grid(row=2, column=1, columnspan=2, pady=10)
    resend_button.config(state="disabled")

    # Start the countdown
    start_countdown(countdown_label, 30)

def send_otp(user_id):
    global verified_number
    
    # Read phone number from CSV
    verified_number = None
    try:
        with open(details_csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["Id"] == user_id:
                    verified_number = row.get("phone_number")
                    if not verified_number:
                        messagebox.showerror("Phone Number Missing", "No phone number found for the given user ID.")
                        return
                    break
            else:
                messagebox.showerror("User Not Found", "User ID not found in database.")
                return

        # Log phone number for debugging
        print(f"Phone Number to Send OTP: {verified_number}")

        # Send OTP via Twilio
        client = get_twilio_client()
        verification = client.verify \
            .v2 \
            .services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel='sms')

        print("Verification SID:", verification.sid)  # Optional: for debugging/logging
        messagebox.showinfo("OTP Sent", "OTP has been sent to your number.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {e}")

def verify_otp():
    global otp_trials, verified_number

    if otp_trials >= 3:
        messagebox.showerror("Locked Out", "Maximum OTP attempts exceeded. Please contact support.")
        otp_window.destroy()
        return

    otp_code = otp_entry.get().strip()  # Strip whitespace from OTP entry
    client = get_twilio_client()

    # Log OTP code and phone number for debugging
    print(f"Verifying OTP Code: {otp_code} for Phone Number: {verified_number}")

    try:
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=verified_number, code=otp_code)
        
        if verification_check.status == "approved":
            messagebox.showinfo("OTP Verified", "OTP verification successful!")
            otp_window.destroy()
            transaction(user_id)  # Call the transaction function with the correct number of arguments
        else:
            otp_trials += 1
            if otp_trials < 3:
                messagebox.showerror("OTP Verification Failed", f"Incorrect OTP. Please try again. Remaining trials: {3 - otp_trials}")
            else:
                messagebox.showerror("Maximum OTP Trials Exceeded", "You have exceeded the maximum number of OTP trials.")
                # Optional: Add action to reset or disable the account temporarily.
    except Exception as e:
        messagebox.showerror("Error", f"Failed to verify OTP: {e}")

def resend_otp():
    global otp_trials
    otp_trials = 0
    send_otp(user_id)
    start_countdown(countdown_label, 30)  # Restart countdown after resend

def start_countdown(label, remaining_time):
    """Countdown from remaining_time seconds and update the label."""
    if remaining_time > 0:
        label.config(text=f"00:{remaining_time:02d}")
        otp_window.after(1000, start_countdown, label, remaining_time - 1)
    else:
        # Allow the user to request another OTP after the countdown
        messagebox.showinfo("OTP Expired", "The OTP has expired. Please request a new OTP.")
        label.config(text="00:00")
        resend_button.config(state="normal")  # Enable the resend OTP button
