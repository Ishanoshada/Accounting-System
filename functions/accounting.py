import json
import time
import uuid
import hashlib

user_file = "data/users.json"

try:
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

def save_data(users):
    with open(user_file, "w") as file:
        json.dump(users, file, indent=4)

# Updated deposit function to accept the user's ID and target user's ID
def deposit(users, user_id, target_id, amount):
    uname, user = find_user(users, user_id)
    tname, target_user = find_user(users, target_id)

    if user and target_user:
        user['balance'] -= amount  # Deduct from the current user's balance
        target_user['balance'] += amount  # Add to the target user's balance

        # Add deposit history to both users
        add_deposit_history(user, target_user, amount)

        save_data(users)
        return tname  # Return the target user's data
    else:
        return None

def withdraw(users, identifier, amount):
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

# Function to add deposit history to users
def add_deposit_history(user, target_user, amount):
    timestamp = int(time.time())
    deposit_info = {
        "timestamp": timestamp,
        "amount": amount,
        "target_user": target_user['id'],
    }
    if 'deposit_history' not in user:
        user['deposit_history'] = []
    user['deposit_history'].append(deposit_info)

# Function to add withdrawal history to users
def add_withdrawal_history(user, amount):
    timestamp = int(time.time())
    withdrawal_info = {
        "timestamp": timestamp,
        "amount": amount,
    }
    if 'withdrawal_history' not in user:
        user['withdrawal_history'] = []
    user['withdrawal_history'].append(withdrawal_info)



def get_deposit_history(user):
  
    return user.get('deposit_history', [])

def get_withdrawal_history(user):
    
    return user.get('withdrawal_history', [])
