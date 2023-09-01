import json,time,uuid
import hashlib
from . import *

user_file = "data/users.json"
try:
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}
    
def data_refresh():
    global users
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
    return str(int((int(time.time())*int(time.time())/(int(time.time())*9))))

# Function to sign up a new user
def signup(users,username, password):
    
    if username in users:
        return "Username already exists. Please choose another."
    
    salt, hashed_password = hash_password(password)
    user_id = generate_id()
    users[username] = {
        "id": user_id,
        "salt": salt,
        "password": hashed_password,
        "balance":0
    }
    save_data(users)
    data_refresh()
    return users[username]

# Function to log in an existing user
def login(users,username, password):
    
    if username not in users:
        return "User does not exist. Please sign up."
    
    stored_password = users[username]["password"]
    salt = users[username]["salt"]
    entered_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    id = users[username]["id"]

    if entered_password == stored_password:
        data_refresh()
        return users[username]
    else:
        return "Incorrect password. Please try again."


