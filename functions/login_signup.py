import json,time,hashlib,base64,os


user_file = "data/users.json"
cookie_file = "data/cookie.txt"
try:
    with open(user_file, "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}
    
def data_refresh(username_):
    global users
    global user_data
    try:
      with open(user_file, "r") as file:
        users = json.load(file)
        
        user_data = users[username_]
        return user_data
    except FileNotFoundError:
      users = {}
      return None

def save_data(users):
    with open(user_file, "w") as file:
        json.dump(users, file, indent=4)
        
def hash_password(password):
    import uuid;salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return (salt, hashed_password)

def generate_id():
    return str(int((int(time.time())*int(time.time())/(int(time.time())*9))))

# Function to sign up a new user
def signup(users,username, password):
    global username_
    username_ = username
    if username in users:
        return "Username already exists. Please choose another."
    
    salt, hashed_password = hash_password(password)
    user_id = generate_id()
    users[username] = {
        "id": user_id,
        "salt": salt,
        "password": hashed_password,
        "balance":0,
        "deposit_history": [],
        "withdrawal_history": [],
    }
    save_data(users)
    
    return users[username]

# Function to log in an existing user
def login(users,username, password):
    global username_
    username_ = username
    if username not in users:
        return "User does not exist. Please sign up."
    
    stored_password = users[username]["password"]
    salt = users[username]["salt"]
    entered_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    id = users[username]["id"]

    if entered_password == stored_password:
        
        return users[username]
    else:
        return "Incorrect password. Please try again."

def logged(username=None, password=None):
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
           # print(data)
            if type(data) == str:
                return False,False
            else:
                return True, True
        else:
            user_credentials = f"{username}::{password}"
 
            fdata = base64.b64encode(user_credentials.encode()).decode()
            open(cookie_file, "wb").write(fdata.encode())
            return username,password
    else:
        if fdata:
            fdata = base64.b64decode(fdata.encode()).decode()
            fdata = fdata.split("::")
        
            data = login(users, fdata[0], fdata[1])
            if type(data) == str:
                return False,False
            else:
                return data,fdata[0]
        else:
            return False,False

def change_password(users, username, old_password, new_password):
    if username not in users:
        return "User does not exist. Please sign up."

    stored_password = users[username]["password"]
    salt = users[username]["salt"]
    entered_password = hashlib.sha256(salt.encode() + old_password.encode()).hexdigest()

    if entered_password == stored_password:
        # Password matches, generate a new password hash
        new_salt, new_hashed_password = hash_password(new_password)
        # Update the user's password and salt
        users[username]["password"] = new_hashed_password
        users[username]["salt"] = new_salt
        save_data(users)
        data_refresh(username)
        os.system("rm -rf data/cookie.txt")
        return "Password changed successfully."
    else:
        return "Incorrect old password. Password change failed."

                  

     
     
    
  
    
#logged("ish","ish")
    
    
    
    
    
