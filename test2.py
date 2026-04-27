from database import add_password, get_all_passwords, search_passwords,delete_password

add_password("Gmail",     "rohit@gmail.com", "ENCRYPTED_123")
add_password("gitHub",    "rohit_dev",       "ENCRYPTED_456")
add_password("Instagram", "@rohit",          "ENCRYPTED_789")

# view all
print("ALL PASSWORDS:")
for p in get_all_passwords():
    print(f"  {p['id']}. {p['account']} — {p['username']}")

# search test
print("\nSEARCH 'git':")
for p in search_passwords("git"):
    print(f"  {p['account']}")

# delete test
delete_password(2)
print("\nAFTER DELETING ID 2:")
for p in get_all_passwords():
    print(f"  {p['id']}. {p['account']}")

