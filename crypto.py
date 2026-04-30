from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import hashlib 

salt = b"say_hello_rohit!!"


# ── FUNCTION 1: derive_key()
def derive_key(master_password: str) -> bytes:
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    raw_key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(raw_key)

# ── FUNCTION 2: get_fernet()
def get_fernet(master_password: str) -> Fernet:
    key = derive_key(master_password)
    return Fernet(key)

# ── FUNCTION 3: encrypt_password()
def encrypt_password(fer: Fernet, password: str) -> str:
    encrypt_bytes = fer.encrypt(password.encode())
    return encrypt_bytes.decode()

# ── FUNCTION 4: decrypt_password()
def decrypt_password(fer: Fernet, encrypted: str) -> str:
    decrypt_bytes = fer.decrypt(encrypted.encode())
    return decrypt_bytes.decode()


# ── FUNCTION 5: check_password_strength()
def check_password_strength(password: str) -> tuple:
    score = 0
    if len(password) >= 8:          # minimum 8 characters → basic requirement
        score += 1

    if any(c.isupper() for c in password):  #any() → returns True if at least ONE character passes
        score+=1                            

    if any(c.islower() for c in password):       
        score+=1

    if any(c.isdigit() for c in password):     
        score+=1

    special = "!@#$%^&*()_+=-[]{}|:;,.?<>"
    if any(c in special for c in password):  # checks if any character exists in our special chars string
        score+=1

# ── SCORE → LABEL + COLOR
    if score <= 2:
        return(score, "WEAK", "#FF4444")
        # 0-2 rules passed → red → password is too simple
    
    if score <=3:
        return(score, "MEDIUM", "#FFD700")
        # 3 rules passed → gold/yellow → getting better

    else:
        return(score, "STRONG" , "#00FF88")
        # 4-5 rules passed → green → great password!

# ── ADD FUNCTION 6: hash_master_key() 
def hash_master_key(master: str) -> str:
    # converts master password → fixed hash string
    # ONE WAY → can never reverse it to get original password
    # same password ALWAYS gives same hash → used for comparison

    return hashlib.sha256(master.encode()).hexdigest()
    # .encode()    → "rohit123" → b"rohit123" (string to bytes)
    # sha256()     → runs hashing algorithm
    # .hexdigest() → converts result to readable string
    # example: "rohit123" → "a665a45920422f..."  (always same!)


# ── ADD FUNCTION 7: verify_master_key() 
def verify_master_key(master: str, stored_hash: str) -> bool:
    # checks if what user typed matches the stored hash
    # returns True  → correct password → let them in
    # returns False → wrong password  → reject!

    return hash_master_key(master) == stored_hash
    # hash what they typed NOW
    # compare with hash saved in vault.json
    # True only if BOTH hashes are identical