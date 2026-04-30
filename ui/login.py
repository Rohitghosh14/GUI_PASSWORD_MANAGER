import customtkinter as ctk             # customtkinter → our GUI library
import sys                              # sys.exit() → closes the entire app
from theme import  COLORS, FONT
from crypto import get_fernet           # get_fernet() → converts master password → Fernet object
import os                               # os.path.exists() → check if vault.json exists
from database import is_vault_setup, setup_master_key, check_master_key
# ── LOGIN SCREEN CLASS

class LoginScreen:

        def __init__(self,parent, on_success):
                
                self.parent = parent             # parent     → the main app window (ctk.CTk())
                self.on_success= on_success      # on_success → a function to call when login works
                self.show_password = False       # tracks visibility state
                self.build_ui()                  #call function that creates all the widgets

        def build_ui(self):                 # creates every widget on the login screen / called once when LoginScreen is created

                # ── MAIN FRAME:
                self.frame = ctk.CTkFrame(                       # CTkFrame → a container that holds other widgets
                        self.parent,
                        fg_color=COLORS["bg_primary"],              # fg_color  → background color = deep black
                        corner_radius=0                             # corner_radius=0 → sharp corners (fills whole window)
                
                )

                self.frame.pack(fill ="both", expand=True)

                # ── LOCK ICON LABEL:
                icon_label = ctk.CTkLabel(
                        self.frame,
                        text="🔐",
                        font=(FONT["family"],48),
                        text_color=COLORS["gold"]
                )
                icon_label.pack(pady=(60,0))
                

                # ── TITLE TEXT:
                title_label =ctk.CTkLabel(
                        self.frame,
                        text="PASSWORD VAULT",
                        font=(FONT["family"],FONT["size_xl"]),
                        text_color=COLORS["blue"]
                )
                title_label.pack(pady=(10,0))
                
                
                if is_vault_setup():
                        subtitle_text = "ENTER MASTER KEY TO CONTINUE"
                else:
                        subtitle_text = "SET YOUR MASTER KEY FOR FIRST TIME"

                subtitle_label = ctk.CTkLabel(
                        self.frame,
                        text="ENTER MASTER KEY TO COUNTINUE",
                        font=(FONT["family"],FONT["size_sm"]),
                        text_color=COLORS["white_dim"]
                )
                subtitle_label.pack(pady=(4,30))
                

                # ── INPUT CONTAINER FRAME 
                input_frame = ctk.CTkFrame(
                        self.frame,
                        fg_color="transparent"
                )
                input_frame.pack(pady=(0,10))
                # transparent → no background color
                # just a container to hold input + eye button side by side

                # ── MASTER KEY INPUT
                self.key_input = ctk.CTkEntry(
                        input_frame,
                        width=260,
                        height=40,
                        placeholder_text="enter master key...",
                        show="꩜",          # show="꩜" → hides text as dots (password field)
                        fg_color=COLORS["bg_secondary"],
                        border_color=COLORS["blue"],
                        text_color=COLORS["white"],
                        placeholder_text_color =COLORS["white_dim"],
                        font=(FONT["family"],FONT["size_md"]),
                        corner_radius=6,
                        border_width=1,
                )
                self.key_input.grid(row=0, column=0 ,padx=(0,6))
                # .grid() → places widget in a grid layout
                # padx=(0, 6) → 0px left, 6px right (gap before eye button)

                self.key_input.bind("<Return>",lambda e: self.attempt_login())
                # bind("<Return>") → listen for Enter key press
                # when Enter pressed → call attempt_login()
                # lambda e: → e is the event object (we don't need it)

                # ── SHOW/HIDE TOGGLE BUTTON:
                self.show_password = False
                # False = hidden (dots) by default

                self.eye_btn = ctk.CTkButton(
                        input_frame,
                        text="👁",
                        width=40,
                        height=40,
                        fg_color=COLORS["bg_secondary"],
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["blue"],
                        border_width=1,
                        corner_radius=6,
                        command=self.toggle_password
                )
                # command → function to call when button clicked
                # toggle_password → shows/hides the master key

                self.eye_btn.grid(row=0,column=1)
                

                # ── ERROR MESSAGE LABEL:
                self.error_label = ctk.CTkLabel(
                        self.frame,
                        text="",                # starts empty → only shows text when login fails
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["danger"]             # danger = red → error messages shown in red
                )
                self.error_label.pack(pady =(0,10))

                # ── UNLOCK BUTTON:

                #  different button text on first run
                btn_text = "[CREATE VAULT]" if not is_vault_setup() else "[UNLOCK]"
                
                unlock_btn = ctk.CTkButton(
                        self.frame,
                        text="[UNLOCK]",
                        width=310,
                        height=42,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["blue"],
                        border_width=1,
                        text_color=COLORS["blue"],
                        font=(FONT["family"],FONT["size_md"]),
                        corner_radius=6,
                        command=self.attempt_login               # calls attempt_login() when clicked
                )
                unlock_btn.pack(pady=(0, 20))

                # ── GOLD DIVIDER LINE
                divider = ctk.CTkFrame(
                        self.frame,
                        width=300,
                        height=1,
                        fg_color=COLORS["gold"]         # thin gold horizontal line — purely decorative
                )
                divider.pack(pady=(0, 14))


                # ── HINT TEXT:
                hint_label= ctk.CTkLabel(
                        self.frame,
                        text="ENCRYPTED WITH FERNET + PBKDF2",
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["white_dim"]
                )
                hint_label.pack()

        # ── TOGGLE PASSWORD VISIBILITY:
        def toggle_password(self):
                # switches master key input between hidden and visible
                # called when user clicks the 👁 eye button
                
                self.show_password = not self.show_password
                # not → flips the boolean
                # False → True  (show password)
                # True  → False (hide password)

                if self.show_password:
                        self.key_input.configure(show="")
                        # show="" → display actual characters typed
                else:
                        self.key_input.configure(show="꩜")
                        # show="꩜" → hide characters as dots


        # ── ATTEMPT LOGIN:
        def attempt_login(self):

                # called when user clicks UNLOCK or presses Enter
                # validates the master key and opens dashboard if correct

                master = self.key_input.get().strip()
                # .get()   → reads current text from input field
                # .strip() → removes accidental spaces at start/end
                if not master:
                        self.error_label.configure(text="⚠ PLEASE ENTER MASTER KEY")
                        return                          
                

                # ── FIRST RUN: no vault set up yet 
                if not is_vault_setup():
                        # is_vault_setup() → False means first time ever
                        # we trust whatever they type → save it as master key

                        if len(master) < 6:
                                # basic minimum length check on first run
                                self.error_label.configure(text="⚠  MINIMUM 6 CHARACTERS")
                                return

                        setup_master_key(master)
                        # database.py: hashes master → saves to vault.json
                        # from now on ONLY this key can open the vault!

                        self.error_label.configure(text="")
                        fer = get_fernet(master)        # create encryption engine
                        self.frame.destroy()
                        self.on_success(fer)            # open dashboard
                        return

                # ── NORMAL LOGIN: vault already set up 
                if not check_master_key(master):
                        # check_master_key() → hashes input → compares with stored hash
                        # False = wrong password → reject!
                        self.error_label.configure(text="⚠  WRONG MASTER KEY")
                        return
                        # frame NOT destroyed → user stays and tries again

                # ── SUCCESS: correct password 
                self.error_label.configure(text="")
                fer = get_fernet(master)            # create encryption engine with correct key
                self.frame.destroy()               # close login screen
                self.on_success(fer)               # open dashboard ✅




        




