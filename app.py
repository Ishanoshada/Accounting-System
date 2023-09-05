# Import necessary modules
import random
import os
import datetime
import json
import base64
import time

# Try to import the 'CurrencyRates' class from the 'forex_python.converter' module.
# If it's not installed, attempt to install it using pip.
try:
    from forex_python.converter import CurrencyRates
except:
    os.system("pip install forex_python ")
    from forex_python.converter import CurrencyRates

# Import functions from other modules
from functions.login_signup import (
    signup,
    login,
    change_password,
    logged,
    data_refresh,
    save_data
)

from functions.accounting import (
    deposit,
    withdraw,
    get_deposit_history,
    get_withdrawal_history,
    export_transactions_to_csv,
)

# Define colors for console output
bcolors = [
    '\033[94m',   # Blue
    '\033[96m',   # Cyan
    '\033[92m',   # Green
    '\033[93m',   # Yellow
    '\033[1;33m', # Bold Yellow
]

# File paths and checking
user_file = "data/users.json"
cookie_file = "data/cookie.txt"
csv_export_file = "data/transactions.csv"

folder_paths = ["data"]
for folder_path in folder_paths:
    os.makedirs(folder_path, exist_ok=True)

# Initialize currency converter
currency_converter = CurrencyRates()

# Initialize users dictionary or load existing user data from a file
try:
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# Function to clear the screen
def clear_screen():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Function for user input
def inputf(output):
    return input(f"\n\n\t\033[1;97m[>] {output}")

# Function to print text with a simulated typing effect
def printf(text, base_delay=0.023, jitter=0.02):
    for char in text:
        delay = max(0, base_delay + random.uniform(-jitter, jitter))

        # Print the character with a small delay
        print(char, end='', flush=True)
        time.sleep(delay)

# Function to create a formatted table
def create_table(text):
    terminal_width = os.get_terminal_size().columns
    border = '*' * (terminal_width - 2)

    text_lines = text.split('\n')
    formatted_text = ''
    for line in text_lines:
        formatted_text += f"| {line.center(terminal_width - 4)} |\n"

    table = f"{border}\n{formatted_text}{border}"

    return table

# Currency Converter function
def convert_currency(username):
    try:
        source_currency = inputf("Enter source currency (e.g., USD): ").upper()
        target_currency = inputf("Enter target currency (e.g., EUR): ").upper()
        amount = float(inputf("Enter the amount to convert: "))

        result = currency_converter.convert(source_currency, target_currency, amount)
        printf(
            f"\n\t Result :> {amount} {source_currency} is approximately {result} {target_currency}")
    except Exception as e:
        print("Error performing currency conversion:", str(e))

# Function for user input with password complexity check
def input_password(output, login=False):
    trying = 1
    while True:
        password = input(f"{output}")
        if is_password_complex(password):
            return password
        else:
            if login:
                trying += 1
                if trying == 4:
                    print("\n\t[+] Entering the password is restricted ")
                    main()
            print("\n\t[+] Password must be at least 6 characters long and contain at least one uppercase letter, one lowercase letter, and one digit. (e.g., inTe1@)")

# Function to check password complexity
def is_password_complex(password):
    if len(password) < 6:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True

# Main function for accounting operations
def accounting_main(user_data, username):
    if user_data:
        while True:
            user_data = data_refresh(username)
            clear_screen()

            # Randomly select text colors
            color1 = random.choice(bcolors)
            color2 = random.choice(bcolors)

            while color1 == color2:
                color2 = random.choice(bcolors)

            printf(color1)
            print(
                create_table(
                    f"\n\tAccount Management ( Your ID: {user_data['id']} and Balance : {user_data['balance']} )\n"
                )
            )
            printf(color2)

            printf("\n\t1. Deposit Money\n", base_delay=0.01)
            printf("\t2. Withdraw Money\n", base_delay=0.01)
            printf("\t3. View Deposit History\n", base_delay=0.01)
            printf("\t4. View Withdrawal History\n", base_delay=0.01)
            printf("\t5. Change Password\n", base_delay=0.01)
            printf("\t6. Export Data\n ", base_delay=0.01)
            printf("\t7. Convert Currency\n", base_delay=0.01)
            printf("\t8. Back\n", base_delay=0.01)
            printf("\t9. Account Delete \n", base_delay=0.01)
            printf("\t10. Logout\n", base_delay=0.01)

            choice = inputf("\tEnter your choice: ")

            if choice == "1":
                amount = float(inputf("\n\tEnter the amount to deposit: "))
                target_id = inputf("\n\tEnter the target user's ID or username: ")
                result = deposit(users, user_data['id'], target_id, amount)
                if result:
                    user_data = data_refresh(username)
                    printf(
                        f"\n\t[+] Deposited {amount} into {result}'s account. New balance: {user_data['balance']}"
                    )
                else:
                    printf("\t [+] User(s) not found.")

            elif choice == "2":
                amount = float(inputf("\n\tEnter the amount to withdraw: "))
                result = withdraw(users, user_data['id'], amount)
                if isinstance(result, str):
                    printf(f"\n\t[+] {result}")
                else:
                    user_data = data_refresh(username)
                    printf(
                        f"\n\t[+] Withdrawn {amount}. New balance: {user_data['balance']}"
                    )

            elif choice == "3":
                deposit_history = get_deposit_history(users[username])
                if deposit_history:
                    printf("\nDeposit History:")
                    for transaction in deposit_history:
                        printf(
                            f"\n\t [×] Timestamp: {transaction['timestamp']}, Amount: {transaction['amount']}, Target User ID: {transaction['target_user']}"
                        )
                else:
                    printf("\n\tNo deposit history.")

            elif choice == "4":
                withdrawal_history = get_withdrawal_history(users[username])
                if withdrawal_history:
                    printf("\nWithdrawal History:")
                    for transaction in withdrawal_history:
                        printf(
                            f"\n\t [×] Timestamp: {transaction['timestamp']}, Amount: {transaction['amount']}"
                        )
                else:
                    printf("\n\tNo withdrawal history.")

            elif choice == "5":
                old_password = input_password(
                    "\n\t\033[1;97m[>] Enter your old password: ")
                new_password = input_password(
                    "\n\t\033[1;97m[>] Enter your new password: ")
                result = change_password(
                    users, username, old_password, new_password)
                printf("\n" + result)

            elif choice == "6":
                if not username:
                    printf("You need to log in to export data.")
                else:
                    export_transactions_to_csv(username)
                    printf(
                        "\n[+] Transaction data exported to CSV file. (data/transactions.csv}")

            elif choice == "7":
                convert_currency(username)

            elif choice == "8":
                break

            elif choice == "9":
                ch = inputf("Do you want to Delete your account? (0-no/1-yes): ")
                if "0" not in ch:
                    del users[username]
                    save_data(users)
                    os.system("rm -rf data/cookie.txt")
                    main()

            elif choice == "10":
                ch = inputf("Do you want to logout? (0-no/1-yes): ")
                if "0" not in ch:
                    os.system("rm -rf data/cookie.txt")
                    main()

            input("\n\n\t :> ")

    else:
        printf("You are not logged in. Please log in or sign up first.")

# Main function for the entire application
def main():
    global username
    while True:
        clear_screen()
        color1 = random.choice(bcolors)
        color2 = random.choice(bcolors)

        while color1 == color2:
            color2 = random.choice(bcolors)

        printf(color1)
        print(
            create_table(
                f"\nWelcome to Accounting System\n  ( by Intelliblitz Team ) \n"
            )
        )
        printf(color2)
        printf("\n\t1. Sign up\n")
        printf("\t2. Log in\n")
        printf("\t3. Quit\n")

        choice = inputf("Enter your choice: ")

        if choice == "1":
            while True:
                username = inputf("Enter your username: ")
                if username:
                    break
                else:
                    printf("\n\t[•] Username is Empty  ! \n")

            password = input_password(
                "\n\t\033[1;97m[>] Enter your password ( length: 6):\033[0m ")
            data = signup(users, username, password)
            if type(data) == str:
                print("")
                printf(data)
                inputf("")
            else:
                printf(
                    "\n\t[•] The password will be saved automatically ! ", base_delay=0.025)
                inputf("")
                accounting_main(data, username)

        elif choice == "2":
            try:
                check, username = logged()
            except Exception as b:
                printf(
                    f"\n\t If the password is correct, the username is incorrect, try again   \n"
                )
                os.system("rm -rf data/cookie.txt")
                inputf("")
                main()

            if check:
                accounting_main(check, username)
            else:
                    while True:
                     username = inputf("Enter your username: ")
                     if username:
                        break
                     else:
                        printf("\n\t[•] Username is Empty  !\n ")

                    password = input_password(
                        "\n\t\033[1;97m[>] Enter your password ( length: 6):\033[0m ", login=True)

                    data = login(users, username, password)

                    if type(data) == str:
                        print("")
                        printf(data)

                        inputf("")

                    else:
                        logged(username, password)
                        printf(
                            "\n\t[•] The password will be saved automatically ! ", base_delay=0.025)
                        inputf("")
                        accounting_main(data, username)

        elif choice == "3":
            break

# Entry point of the application
def run():
    try:
        main()
        printf(
            "\n [•] Thank you for using CLI Accounting system ( by Intelliblitz Team ). Goodbye!")
        exit()
    except:
        pass
    
        

# Check if the script is being run directly
if __name__ == "__main__":
    run()
