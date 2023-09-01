from functions.login_signup import *


if __name__ == "__main__":
    while True:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n\tWelcome to CLI Bancking System ")
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        print("\t\t1. Sign up")
        print("\t\t2. Log in")
        print("\t\t3. Quit\n")
        
        choice = input("\tEnter your choice: ")
        
        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            result = signup(users,username, password)
            print(result)
        
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            result = login(users,username, password)
            print(result)
        
        elif choice == "3":
            break


