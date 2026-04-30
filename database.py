import json                         
import os                           
from datetime import datetime
import hashlib


# ── FILE NAME:
DB_FILE = "vault.json"              

# ── FUNCTION 1: load_data()
def load_data() -> dict:                 
    if not os.path.exists(DB_FILE):      # os.path.exists() → checks if vault.json is on disk
        return {"passwords":[]}
    

    with open(DB_FILE,"r") as f:

        return json.load(f)             
    

# ── FUNCTION 2: save_data():
def save_data(data: dict):              
    with open(DB_FILE,"w") as f:       
        json.dump(data, f, indent=4)    


# ── FUNCTION 3: get_all_passwords():

def get_all_passwords() -> list:         
    data = load_data()
    return data["passwords"]            

# ── FUNCTION 4: add_password():

def add_password(account: str, username: str, encrypted_password: str):

    data = load_data()          
    passwords = data["passwords"]       

    new_id = len(passwords)+1

    new_entry = {
        "id":       new_id,
        # unique number to identify this entry

        "account":      account,
        # site or app name → "Gmail", "Instagram" etc

        "username":     username,
        # email or username for that account

        "password":     encrypted_password,
        # looks like: "gAAAAABhxyz123..."

        "data_added": datetime.now().strftime("%Y-%m-%d %H:%M"),
        # datetime.now() → current date and time
        # .strftime() → formats it as a readable string
        # "%Y-%m-%d %H:%M" → "2024-01-15 10:30"
    }
    passwords.append(new_entry)
    

    save_data(data)
    

# ── FUNCTION 5: delete_password()
def delete_password(entry_id: int):

    data = load_data()          

    data["passwords"] = [
        p for p in data["passwords"] if p["id"] != entry_id
    ]

    save_data(data)

# ── FUNCTION 6: search_passwords()
def search_passwords(query: str) -> list:
    
    all_passwords = get_all_passwords()           

    query = query.lower()                          


    return[ p for p in all_passwords if query in p["account"].lower() 
        or query in p["username"].lower() ]

    # keeps entry if query found in account name OR username
    # p["account"].lower() → "Gmail" becomes "gmail"
    # query in "gmail"     → True if "gm" is inside "gmail"

# ── FUNCTION 7: is_vault_setup()


def is_vault_setup() -> bool:
    # checks if master key has EVER been set before
    # returns True  → vault exists + master hash stored → show login
    # returns False → first run ever → let user set master key

    if not os.path.exists(DB_FILE):
        return False
        # no vault.json at all → definitely first run

    data = load_data()
    return "master_hash" in data
    # master_hash key present in JSON → vault is set up ✅
    # master_hash key missing         → first run ❌



# ── FUNCTION 8: setup_master_key()


def setup_master_key(master: str):
    # called ONCE on very first run
    # hashes and permanently stores the master key
    # NEVER stores the actual password — only its hash!

    data = load_data()
    # load existing data (even if empty {"passwords": []})

    data["master_hash"] = hashlib.sha256(master.encode()).hexdigest()
    # hashlib.sha256()  → hashing algorithm (one way — cannot reverse!)
    # .encode()         → "rohit123" → b"rohit123" (string to bytes)
    # .hexdigest()      → converts hash result to readable string
    # example: "rohit123" → "a665a45920422f9d417e4867efdc4fb8..."

    save_data(data)
    # vault.json now looks like:
    # {
    #     "master_hash": "a665a45920422f...",
    #     "passwords": []
    # }


# ── FUNCTION 9: check_master_key()

def check_master_key(master: str) -> bool:
    # called on EVERY login attempt after first run
    # hashes what user typed → compares with stored hash
    # returns True  → correct password → open vault 
    # returns False → wrong password  → reject 

    data = load_data()

    stored_hash = data.get("master_hash", "")
    # .get("master_hash", "") → safely gets hash from JSON
    # if key missing → returns "" instead of crashing

    entered_hash = hashlib.sha256(master.encode()).hexdigest()
    # hash what user typed RIGHT NOW
    # same algorithm as setup_master_key() → produces same hash
    # if same password typed → same hash produced 

    return entered_hash == stored_hash
    # True  → hashes match → correct password → let them in
    # False → hashes differ → wrong password  → block them







