from crypto import get_fernet, encrypt_password, decrypt_password

fer = get_fernet("testmaster")
enc = encrypt_password(fer, "myPassword123")
dec = decrypt_password(fer, enc)
print(dec)