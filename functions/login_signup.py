import json,uuid
import hashlib
from . import *

user_file = "data/users.json"
try:
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

def save_data(users):
    with open(user_file, "w") as file:
        json.dump(users, file, indent=4)
        
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return (salt, hashed_password)

def generate_id():
    return str(uuid.uuid4())

# Function to sign up a new user
def signup(users,username, password):
    
    if username in users:
        return "Username already exists. Please choose another."
    
    salt, hashed_password = hash_password(password)
    user_id = generate_id()
    users[username] = {
        "id": user_id,
        "salt": salt,
        "password": hashed_password
    }
    save_data(users)
    return "Signup successful. Your ID is: {}".format(user_id)

# Function to log in an existing user
def login(users,username, password):
    
    if username not in users:
        return "User does not exist. Please sign up."
    
    stored_password = users[username]["password"]
    salt = users[username]["salt"]
    entered_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()

    if entered_password == stored_password:
        return "Login successful. Welcome, {}!".format(username)
    else:
        return "Incorrect password. Please try again."

