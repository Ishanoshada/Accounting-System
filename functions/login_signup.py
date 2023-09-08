import json
import time
import hashlib
import base64
import os
import uuid  # Import UUID module for generating salts

# File paths for user data and cookie
user_file = "data/users.json"
cookie_file = "data/cookie.txt"

try:
    # Load user data from the file if it exists
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    # Initialize an empty users dictionary if the file doesn't exist
    users = {}


def data_refresh(username_):
    """
    Refresh user data from the file and return user_data for a given username.

    Args:
        username_: The username to retrieve data for.

    Returns:
        user_data: User data for the specified username.
    """
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


def save_data(users):
    """
    Save the users dictionary to the user data file.

    Args:
        users: The dictionary containing user data.
    """
    try:
        # Save the users dictionary to the user data file
        with open(user_file, "w") as file:
            json.dump(users, file, indent=4)
    except:
        return {}


def hash_password(password):
    """
    Hash a password and generate a salt.

    Args:
        password: The password to hash.

    Returns:
        salt: The generated salt.
        hashed_password: The hashed password.
    """
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(
        salt.encode() + password.encode()).hexdigest()
    return salt, hashed_password


def generate_id():
    """
    Generate a unique user ID.

    Returns:
        user_id: The generated user ID.
    """
    return str(int((int(time.time()) * int(time.time()) / (int(time.time()) * 9))))


def signup(users, username, password):
    """
    Handle user registration (signup).

    Args:
        users: The dictionary containing user data.
        username: The desired username.
        password: The user's password.

    Returns:
        user_data: User data for the newly signed-up user.
    """
    global username_
    username_ = username
    if username in users:
        return "\n\tUsername already exists. Please choose another."

    salt, hashed_password = hash_password(password)
    user_id = generate_id()
    users[username] = {
        "id": user_id,
        "salt": salt,
        "password": hashed_password,
        "balance": 0,
        "deposit_history": [],
        "withdrawal_history": [],
    }
    save_data(users)
    return users[username]


def login(users, username, password):
    """
    Handle user login.

    Args:
        users: The dictionary containing user data.
        username: The user's username.
        password: The user's password.

    Returns:
        user_data: User data for the logged-in user if successful, or an error message if not.
    """
    try:
        global username_
        username_ = username
        if username not in users:
            return "\n\tUser does not exist. Please sign up."

        stored_password = users[username]["password"]
        salt = users[username]["salt"]
        entered_password = hashlib.sha256(
            salt.encode() + password.encode()).hexdigest()
        id = users[username]["id"]

        if entered_password == stored_password:
            return users[username]
        else:
            return "\n\tIncorrect password. Please try again."
    except:
        return "\n\tUser does not exist. Please sign up."


def logged(username=None, password=None):
    """
    Check if a user is logged in based on the presence of a cookie file.

    Args:
        username: The username to check.
        password: The user's password.

    Returns:
        (user_data, username): User data and username if logged in, or (False, False) if not.
    """
    try:
        try:
            fdata = open(cookie_file, 'rb').read()
            fdata = fdata.decode()
        except FileNotFoundError:
            fdata = ""

        if username:
            if fdata:
                fdata = base64.b64decode(fdata.encode()).decode()
                fdata = fdata.split("::")

                data = login(users, fdata[0], fdata[1])
                if type(data) == str:
                    return False, False
                else:
                    return True, True
            else:
                user_credentials = f"{username}::{password}"

                fdata = base64.b64encode(user_credentials.encode()).decode()
                open(cookie_file, "wb").write(fdata.encode())
                return username, password
        else:
            if fdata:
                fdata = base64.b64decode(fdata.encode()).decode()
                fdata = fdata.split("::")

                data = login(users, fdata[0], fdata[1])
                if type(data) == str:
                    return False, False
                else:
                    return data, fdata[0]
            else:
                return False, False
    except:
        return False, False


def change_password(users, username, old_password, new_password):
    """
    Change a user's password.

    Args:
        users: The dictionary containing user data.
        username: The username of the user.
        old_password: The old password.
        new_password: The new password.

    Returns:
        message: A success or error message.
    """
    try:
        if username not in users:
            return "\n\tUser does not exist. Please sign up."

        stored_password = users[username]["password"]
        salt = users[username]["salt"]
        entered_password = hashlib.sha256(
            salt.encode() + old_password.encode()).hexdigest()

        if entered_password == stored_password:
            # Password matches, generate a new password hash
            new_salt, new_hashed_password = hash_password(new_password)
            # Update the user's password and salt
            users[username]["password"] = new_hashed_password
            users[username]["salt"] = new_salt
            save_data(users)
            data_refresh(username)
            os.system("rm -rf data/cookie.txt")
            return "\n\tPassword changed successfully."
        else:
            return "\n\tIncorrect old password. Password change failed."
    except:
        return "\n\tUser does not exist. Please sign up."
