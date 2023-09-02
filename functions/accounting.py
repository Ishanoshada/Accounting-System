import json
import time
import hashlib
import datetime

# File path for storing user data
user_file = "data/users.json"

try:
    # Load user data from the file if it exists
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    # Initialize an empty users dictionary if the file doesn't exist
    users = {}

def save_data(users):
    # Save the users dictionary to the user data file
    with open(user_file, "w") as file:
        json.dump(users, file, indent=4)

def deposit(users, user_id, target_id, amount):
    # Function to handle deposit operations
    uname, user = find_user(users, user_id)
    tname, target_user = find_user(users, target_id)

    if user and target_user:
        if tname == uname:
            pass
        else:
            user['balance'] -= amount  # Deduct from the current user's balance
        target_user['balance'] += amount  # Add to the target user's balance

        # Add deposit history to both users
        add_deposit_history(user, target_user, amount)

        save_data(users)
        return tname  # Return the target user's data
    else:
        return None

def withdraw(users, identifier, amount):
    # Function to handle withdrawal operations
    i, user = find_user(users, identifier)
    if user:
        if user['balance'] >= amount:
            user['balance'] -= amount

            # Add withdrawal history to the user
            add_withdrawal_history(user, amount)

            save_data(users)
            return user  # Return the user data
        else:
            return "Insufficient balance."
    else:
        return None

# Helper function to find a user by ID or username
def find_user(users, identifier):
    for i in users:
        if users[i]['id'] == identifier or i == identifier:
            return i, users[i]
    return None

def add_deposit_history(user, target_user, amount):
    # Function to add deposit history to users
    timestamp = int(time.time())
    deposit_info = {
        "timestamp": str(datetime.datetime.now()),
        "amount": amount,
        "target_user": target_user['id'],
    }
    if 'deposit_history' not in user:
        user['deposit_history'] = []
    user['deposit_history'].append(deposit_info)

def add_withdrawal_history(user, amount):
    # Function to add withdrawal history to users
    timestamp = int(time.time())
    withdrawal_info = {
        "timestamp": timestamp,
        "amount": amount,
    }
    if 'withdrawal_history' not in user:
        user['withdrawal_history'] = []
    user['withdrawal_history'].append(withdrawal_info)

def get_deposit_history(user):
    # Function to get deposit history for a user
    return user.get('deposit_history', [])

def get_withdrawal_history(user):
    # Function to get withdrawal history for a user
    return user.get('withdrawal_history', [])
