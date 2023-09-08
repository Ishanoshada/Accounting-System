import json
import time
import datetime
import csv

# File path for storing user data
user_file = "data/users.json"
csv_export_file = "data/transactions.csv"

try:
    # Load user data from the file if it exists
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    # Initialize an empty users dictionary if the file doesn't exist
    users = {}


def save_data(users):
    """
    Save the users dictionary to the user data file.

    Args:
        users: The dictionary containing user data.
    """
    with open(user_file, "w") as file:
        json.dump(users, file, indent=4)


def deposit(users, user_id, target_id, amount):
    """
    Handle deposit operations.

    Args:
        users: The dictionary containing user data.
        user_id: The user's ID.
        target_id: The target user's ID.
        amount: The amount to deposit.

    Returns:
        target_username: The username of the target user or None if not found.
    """
    uname, user = find_user(users, user_id)
    tname, target_user = find_user(users, target_id)

    if user and target_user:
        if tname != uname:
            user['balance'] -= amount  # Deduct from the current user's balance
        target_user['balance'] += amount  # Add to the target user's balance

        # Add deposit history to both users
        add_deposit_history(user, target_user, amount)

        save_data(users)
        return tname  # Return the target user's username
    else:
        return None


def withdraw(users, identifier, amount):
    """
    Handle withdrawal operations.

    Args:
        users: The dictionary containing user data.
        identifier: The user's ID or username.
        amount: The amount to withdraw.

    Returns:
        result: User data for the user if successful, or an error message if not.
    """
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


def data_refresh(username_):
    global users
    try:
        # Load user data from the file if it exists
        with open(user_file, "r") as file:
            users = json.load(file)

            # Retrieve the user's data based on the username
            user_data = users.get(username_)
            return user_data
    except FileNotFoundError:
        # Initialize an empty users dictionary if the file doesn't exist
        users = {}
        return None


def find_user(users, identifier):
    """
    Find a user by ID or username.

    Args:
        users: The dictionary containing user data.
        identifier: The user's ID or username.

    Returns:
        username: The username if found, or None if not.
        user: User data if found, or None if not.
    """
    for username, user in users.items():
        if user['id'] == identifier or username == identifier:
            return username, user
    return None, None


def add_deposit_history(user, target_user, amount):
    """
    Add deposit history to users.

    Args:
        user: The user making the deposit.
        target_user: The target user receiving the deposit.
        amount: The amount being deposited.
    """
    timestamp = str(datetime.datetime.now())
    deposit_info = {
        "timestamp": timestamp,
        "amount": amount,
        "target_user": target_user['id'],
    }
    if 'deposit_history' not in user:
        user['deposit_history'] = []
    user['deposit_history'].append(deposit_info)


def add_withdrawal_history(user, amount):
    """
    Add withdrawal history to users.

    Args:
        user: The user making the withdrawal.
        amount: The amount being withdrawn.
    """
    timestamp = str(datetime.datetime.now())
    withdrawal_info = {
        "timestamp": timestamp,
        "amount": amount,
    }
    if 'withdrawal_history' not in user:
        user['withdrawal_history'] = []
    user['withdrawal_history'].append(withdrawal_info)


def get_deposit_history(user):
    """
    Get deposit history for a user.

    Args:
        user: The user for whom to retrieve deposit history.

    Returns:
        deposit_history: List of deposit history entries.
    """
    return user.get('deposit_history', [])


def get_withdrawal_history(user):
    """
    Get withdrawal history for a user.

    Args:
        user: The user for whom to retrieve withdrawal history.

    Returns:
        withdrawal_history: List of withdrawal history entries.
    """
    return user.get('withdrawal_history', [])


def export_transactions_to_csv(username):
    """
    Export user's transaction history to a CSV file.

    Args:
        username: The username of the user to export data for.

    Returns:
        csv_export_file: The path to the exported CSV file.
    """
    user_data = data_refresh(username)
    deposit_history = get_deposit_history(user_data)
    withdrawal_history = get_withdrawal_history(user_data)

    # Combine deposit and withdrawal history
    transactions = deposit_history + withdrawal_history

    # Write transactions to a CSV file
    with open(csv_export_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Transaction Type', 'Amount'])
        for transaction in transactions:
            transaction_type = "Deposit" if "target_user" in transaction else "Withdrawal"
            writer.writerow([transaction['timestamp'],
                            transaction_type, transaction['amount']])
        return csv_export_file
