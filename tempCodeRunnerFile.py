# Example usage with raw string
file_path = r'E:\KELLY\PROJECTS\ODL\Final_Year_Project\ATM-Security-Face-Recognition-OTP\Security - Copy (2)\login-verification-master\data.txt'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        print(data)
except FileNotFoundError:
    print("The file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
