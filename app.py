from functions.login_signup import *
from functions.accounting import *
import getpass

# Function for user input
def inputf(output):
    return input(output)

# Function for the main accounting operations
def accounting_main(user_data):
    if user_data:
        while True:
            data_refresh()
            print("\n**********************************************")
            print(f"\n\tAccount Management ( Your ID: {user_data['id']} and Balance : {user_data['balance']} )")
            print("\n**********************************************\n")
            print("\t1. Check Balance")
            print("\t2. Deposit Money")
            print("\t3. Withdraw Money")
            print("\t4. Log Out\n")

            choice = inputf("\tEnter your choice: ")

            if choice == "1":
                print(f"\n\t [+] Your current balance is: {user_data['balance']}")

            elif choice == "2":
                amount = float(inputf("\n\tEnter the amount to deposit: "))
                target_id = inputf("\n\tEnter the target user's ID or username: ")
                result = deposit(users, user_data['id'], target_id, amount)
               # print(result)
                if result:
                    print(f"\n\t[+]Deposited {amount} into {result}'s account. New balance: {user_data['balance']}")
                else:
                    print("\t [+] User(s) not found.")

            elif choice == "3":
                amount = float(inputf("\n\tEnter the amount to withdraw: "))
                result = withdraw(users, user_data['id'], amount)
                print(f"\n\t[+]New balance: {user_data['balance']}")
            #    print(result)

            elif choice == "4":
                break
    else:
        print("You are not logged in. Please log in or sign up first.")

# Function for the main program
def main():
    while True:
        data_refresh()
        print("\n**********************************************")
        print("\n\tWelcome to CLI Banking System")
        print("\n**********************************************\n")
        print("\t1. Sign up")
        print("\t2. Log in")
        print("\t3. Quit\n")
        
        choice = inputf("\tEnter your choice: ")
        
        if choice == "1":
            username = inputf("\n\tEnter your username: ")
            password = getpass.getpass("\n\tEnter your password: ")
            data = signup(users, username, password)
            accounting_main(data)
        
        elif choice == "2":
            username = inputf("\n\tEnter your username: ")
            password = getpass.getpass("\n\tEnter your password: ")
            data = login(users, username, password)
            accounting_main(data)

        elif choice == "3":
            break

if __name__ == "__main__":
    main()
