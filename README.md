# GUI_PASSWORD_MANAGER
# 🔐 Password Vault

A secure, offline desktop password manager built with Python and CustomTkinter.
Passwords are encrypted with industry-standard cryptography — your master key never leaves your machine.

---

## 📸 Preview

> *Login Screen → Master Key Authentication → Password Dashboard*

```
┌─────────────────────────┐      ┌──────────────────────────────────────┐
│         🔐              │      │  🔐 PASSWORD VAULT          [+ADD] [LOCK] │
│    PASSWORD VAULT       │  ──▶ │  ──────────────────────────────────  │
│  ENTER MASTER KEY       │      │  SEARCH ACCOUNTS.....                │
│  [enter master key...👁]│      │  ┌──────────────────────────────┐   │
│       [UNLOCK]          │      │  │ GMAIL          👁  ⧉  ✕      │   │
│  ─────────────────────  │      │  │ rohit@gmail.com               │   │
│  ENCRYPTED WITH FERNET  │      │  │ ••••••••                      │   │
└─────────────────────────┘      │  └──────────────────────────────┘   │
                                 └──────────────────────────────────────┘
```

---

## ✨ Features

- **Master Key Authentication** — Single password protects the entire vault
- **First-Run Setup** — Automatically detects first launch and creates the vault
- **Fernet Encryption** — Every saved password is AES-128 encrypted before storage
- **Password Strength Meter** — Live 5-rule scorer with color-coded bar
- **Show / Hide Passwords** — Toggle visibility per entry with the 👁 button
- **Clipboard Copy** — One-click copy with automatic 30-second clipboard wipe
- **Search** — Real-time filter across account names and usernames
- **Delete Entries** — Permanently remove any saved password
- **Lock & Re-login** — Lock button returns to login screen without closing the app
- **Offline Only** — Zero network calls, zero cloud sync, your data stays local

---

## 🛡️ Security Architecture

```
Master Password (typed by user)
        │
        ▼
  PBKDF2HMAC (100,000 iterations, SHA-256, fixed salt)
        │
        ▼
  32-byte derived key  ──▶  Fernet object (AES-128-CBC + HMAC-SHA256)
        │                          │
        ▼                          ▼
  SHA-256 hash              encrypt / decrypt
  stored in vault.json      individual passwords
  (for login verification)
```

**Key design decisions:**

| What | Why |
|------|-----|
| PBKDF2HMAC with 100,000 iterations | Slows down brute-force attacks on the master key |
| SHA-256 hash stored, not the master key | Even if vault.json is stolen, master key cannot be recovered |
| Fernet encryption per password | Each password gets authenticated encryption (tamper-proof) |
| Clipboard auto-wipe after 30s | Prevents passwords lingering in clipboard after use |
| No network calls | Zero attack surface from internet |

> ⚠️ **Note:** This project uses a fixed salt (`b"say_hello_rohit!!"`) for the KDF. For production use, a random per-user salt stored in `vault.json` would be stronger.

---

## 🗂️ Project Structure

```
GUI_PASSWORD_MANAGER/
│
├── main.py              # Entry point — window setup and screen routing
├── theme.py             # Global color palette and font constants
├── crypto.py            # All encryption, decryption, hashing, and strength logic
├── database.py          # All JSON read/write and vault management logic
│
├── ui/
│   ├── __init__.py      # Makes ui/ a Python package
│   ├── login.py         # LoginScreen class — master key entry and validation
│   └── dashbord.py      # Dashboard class — password list, add, search, delete
│
├── vault.json           # Encrypted data store (auto-created on first run)
├── test.py              # Manual test for crypto module
├── test2.py             # Manual test for database module
└── README.md            # This file
```

---

## 🔧 Tech Stack

| Library | Purpose |
|---------|---------|
| `customtkinter` | Modern themed GUI widgets |
| `cryptography` | Fernet encryption + PBKDF2HMAC key derivation |
| `pyperclip` | Cross-platform clipboard access |
| `hashlib` | SHA-256 master key hashing |
| `json` | Vault data storage |
| `datetime` | Timestamp for saved entries |

---

## ⚙️ Installation

**Prerequisites:** Python 3.8+

```bash
# 1. Clone the repository
git clone https://github.com/your-username/GUI_PASSWORD_MANAGER.git
cd GUI_PASSWORD_MANAGER

# 2. Install dependencies
pip install customtkinter cryptography pyperclip

# 3. Run the app
python main.py
```

---

## 🚀 Usage

### First Launch
1. Run `python main.py`
2. The vault detects no existing data → prompts **"SET YOUR MASTER KEY FOR FIRST TIME"**
3. Enter a master key (minimum 6 characters) and click **[CREATE VAULT]**
4. Your vault is created and you land on the dashboard

### Adding a Password
1. Click **[+ ADD]** in the top-right header
2. Fill in Account Name, Username/Email, and Password
3. Watch the strength meter update live as you type
4. Click **[SAVE PASSWORD]** — it encrypts and stores the entry

### Using Saved Passwords
| Button | Action |
|--------|--------|
| 👁 | Toggle show/hide the decrypted password |
| ⧉ | Copy password to clipboard (auto-clears after 30s) |
| ✕ | Permanently delete the entry |

### Locking the Vault
Click **[LOCK]** in the header — returns to login screen. The Fernet key is destroyed from memory.

---

## 📁 vault.json Structure

```json
{
    "master_hash": "5d150f99ea842f65acb33d4d3c...",
    "passwords": [
        {
            "id": 1,
            "account": "Gmail",
            "username": "rohit@gmail.com",
            "password": "gAAAAABpvXHq8VxVMUHb7QoG...",
            "data_added": "2026-03-20 21:42"
        }
    ]
}
```

- `master_hash` — SHA-256 hash of your master key. Used for login verification only.
- `password` field — Always stored as a Fernet-encrypted string, never plain text.

---

## 🧪 Running Tests

```bash
# Test encryption/decryption round-trip
python test.py

# Test database add / search / delete operations
python test2.py
```

---

## 🗺️ Possible Future Improvements

- [ ] Random salt per vault (stronger KDF)
- [ ] Password generator built into the add form
- [ ] Edit existing password entries
- [ ] Export vault as encrypted backup file
- [ ] Auto-lock after inactivity timeout
- [ ] Dark / Light theme toggle

---

## 👨‍💻 Author

**Rohit** — Python & AI/ML Engineering student  
Built as a portfolio project to demonstrate applied cryptography, GUI development, and secure data storage in Python.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).