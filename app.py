from functions.login_signup import *
from functions.accounting import *
import getpass,random,os,datetime 


    
bcolors = [
    '\033[94m',
     '\033[96m',
     '\033[92m',
     '\033[93m',
     '\033[1;33m',
     ]     
         

def clear_screen():
    # Check if the operating system is Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Function for user input
def inputf(output):
    return input(f"\n\t\033[1;97m[>] {output}")
    
def printf(text, base_delay=0.025, jitter=0.02):
    for char in text:
        delay = max(0, base_delay + random.uniform(-jitter, jitter))
        
        # Print the character with a small delay
        print(char, end='', flush=True)
        time.sleep(delay)
    
def create_table(text):
   
    terminal_width = os.get_terminal_size().columns

    border = '*' * (terminal_width - 2)

    text_lines = text.split('\n')
    formatted_text = ''
    for line in text_lines:
        formatted_text += f"| {line.center(terminal_width - 4)} |\n"

    table = f"{border}\n{formatted_text}{border}"

    return table
    
# Function for the main accounting operations
def accounting_main(user_data, username):
    
    
    if user_data:
        while True:
           user_data = data_refresh(username)
           clear_screen()

           
           color1 = random.choice(bcolors)
           color2 = random.choice(bcolors)
           
           while color1 == color2:
             color2 = random.choice(bcolors)
           printf(color1)
           print(create_table(f"\n\tAccount Management ( Your ID: {user_data['id']} and Balance : {user_data['balance']} )\n"))
           printf(color2)
           
           
           printf("\n\t1. Deposit Money\n")
           printf("\t2. Withdraw Money\n")
           printf("\t3. View Deposit History\n")
           printf("\t4. View Withdrawal History\n")
           printf("\t5. Change Password\n")
           printf("\t6. Quit\n")
           printf("\t7. Logout\n")

           choice = inputf("\tEnter your choice: ")

          

           if choice == "1":
                amount = float(inputf("\n\tEnter the amount to deposit: "))
                target_id = inputf("\n\tEnter the target user's ID or username: ")
                result = deposit(users, user_data['id'], target_id, amount)
               # printf(result)
                if result:
                    printf(f"\n\t[+]Deposited {amount} into {result}'s account. New balance: {user_data['balance']}")
                else:
                    printf("\t [+] User(s) not found.")

           elif choice == "2":
                amount = float(inputf("\n\tEnter the amount to withdraw: "))
                result = withdraw(users, user_data['id'], amount)
                if isinstance(result, str):
                    printf(f"\n\t[+] {result}")
                else:
                  printf(f"\n\t[+] Withdrawn {amount}. New balance: {user_data['balance']}")
                 
            #    printf(result)

           elif choice == "3":
            deposit_history = get_deposit_history(users[username])
            if deposit_history:
                printf("\nDeposit History:")
                for transaction in deposit_history:
                    printf(f"\n\tTimestamp: {transaction['timestamp']}, Amount: {transaction['amount']}, Target User ID: {transaction['target_user']}")
            else:
                printf("\nNo deposit history.")
                
           elif choice == "4":
            withdrawal_history = get_withdrawal_history(users[username])
            if withdrawal_history:
                printf("\nWithdrawal History:")
                for transaction in withdrawal_history:
                    printf(f"\n\tTimestamp: {transaction['timestamp']}, Amount: {transaction['amount']}")
            else:
                printf("\nNo withdrawal history.")
           elif choice == "5":
               
               old_password = getpass.getpass("\n\t\033[1;97m[>] Enter your old password: ")
               new_password = getpass.getpass("\n\t\033[1;97m[>] Enter your new password: ")
               result = change_password(users, username, old_password, new_password)
               printf("\n"+result)

           elif choice == "6":
             break        
                 
           
               
           elif choice == "7":
               ch = inputf("Do you want to be logout?(0-no/1): ")
               if not "0" in ch:
                   os.system("rm -rf data/cookie.txt")
                   main()

           input("\n\n\t :> ")
           
            
    else:
        printf("You are not logged in. Please log in or sign up first.")

# Function for the main program
def main():
    global username
    while True:
        clear_screen()
        color1 = random.choice(bcolors)
        color2 = random.choice(bcolors)
        while color1 == color2:
         color2 = random.choice(bcolors)
        printf(color1)
        print(create_table(f"\nWelcome to  Accounting System\n  ( by Intelliblitz Team ) \n"))
        printf(color2)
        printf("\n\t1. Sign up\n")
        printf("\t2. Log in\n")
        printf("\t3. Quit\n")
        
        choice = inputf("Enter your choice: ")
        
        if choice == "1":
            username = inputf("Enter your username: ")
            password = getpass.getpass("\n\t\033[1;97m[>] Enter your password:\033[0m ")
            data = signup(users, username, password)
            if type(data) == str:
              printf(data)
            else:
             accounting_main(data,username)
        
        elif choice == "2":
           try:
            check, username = logged()
            #printf(username)
           except Exception as b:
            printf(f"\n\t If the password is correct, the username is incorrect, try again   ")
            os.system("rm -rf data/cookie.txt")
            inputf("")
            main ()
           
           if check:
             accounting_main(check,username)
           else:
            
            username = inputf("Enter your username: ")
            password = getpass.getpass("\n\t\033[1;97m[>] Enter your password:\033[0m ")
            data = login(users, username, password)
            
            if type(data) == str:
              printf(data)
              
            else:
             logged(username,password)
             accounting_main(data,username)

        elif choice == "3":
            
            break

if __name__ == "__main__":
  
    main()
    printf("\n [•] Thank you for using CLI Accounting system ( by Intelliblitz Team ). Goodbye!")
    
