import customtkinter as ctk
import pyperclip           # pyperclip → copies text to clipboard / pyperclip.copy("text") → puts text in clipboard
# install with: pip install pyperclip

from theme import COLORS, FONT
from crypto import encrypt_password,decrypt_password,check_password_strength
# encrypt_password()        → locks a password before saving
# decrypt_password()        → unlocks a password to show it
# check_password_strength() → scores password strength 0-5
from database import add_password,get_all_passwords,delete_password,search_passwords
# add_password()      → saves new entry to vault.json
# get_all_passwords() → loads all entries from vault.json
# delete_password()   → removes entry by id from vault.json
# search_passwords()  → filters entries by search query

#--DASHBOARD CLASS:
class Dashboard:
# add_password()      → saves new entry to vault.json
# get_all_passwords() → loads all entries from vault.json
# delete_password()   → removes entry by id from vault.json
# search_passwords()  → filters entries by search query

        def __init__(self,parent,fer):
                self.parent = parent
                self.fer = fer 
                self.showing_passwords = {}
                # dictionary to track which passwords are visible
                # key   = entry id
                # value = True (showing) or False (hidden)
                # example: {1: False, 2: True, 3: False}

                self.clipboard_timer = None
                # stores the timer that clears clipboard after 30s
                # None = no active timer right now

                self.build_ui()
                #build all widgets

        def build_ui(self):
                #-- MAIN FRAME:
                self.frame = ctk.CTkFrame(
                        self.parent,
                        fg_color=COLORS["bg_primary"],
                        corner_radius=0
                )
                self.frame.pack(fill="both", expand= True)

                #--HEADER BAR:
                header = ctk.CTkFrame(
                        self.frame,
                        fg_color=COLORS["bg_secondary"],
                        corner_radius=0,
                        height=48,
                        border_width=1,
                        border_color=COLORS["bg_tertiary"]
                )
                header.pack(fill = "x")
                #fill = "x" -> stretches across full width only 
                header.pack_propagate(False)
                # pack_propagate(False) → keeps fixed height of 48px
                # without this → frame shrinks to fit its children

                #--HEADER TITLE:
                ctk.CTkLabel(
                        header,
                        text="🔐  PASSWORD VAULT",
                        font=(FONT["family"], FONT["size_md"]),
                        text_color=COLORS["blue"],
                ).pack(side="left", padx=16)       # side="left" → sticks to left side of header
                
                #--lOCK BUTTON(TOP RIGHT):
                ctk.CTkButton(
                        header,
                        text="lock",
                        width=70,
                        height=30,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["danger"],
                        border_width=1,
                        text_color=COLORS["danger"],
                        font=(FONT["family"],FONT["size_sm"]),
                        corner_radius=4,
                        command=self.lock_app
                ).pack(side="right",padx=10)

                #--ADD BUTTON(TOP RIGHT):
                ctk.CTkButton(
                        header,
                        text="+ ADD",
                        width=70,
                        height=30,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["gold"],
                        border_width=1,
                        text_color=COLORS["gold"],
                        font=(FONT["family"], FONT["size_sm"]),
                        corner_radius=4,
                        command=self.toggle_add_form
                ).pack(side="right",padx=(0,6))

                #--SEARCH BAR:
                search_frame = ctk.CTkFrame(
                        self.frame,
                        fg_color="transparent"
                )
                search_frame.pack(fill="x", padx=16 , pady=(12, 6))

                self.search_input = ctk.CTkEntry(
                        search_frame,
                        placeholder_text="SEARCH ACCOUNTS.....",
                        height=36,
                        fg_color=COLORS["bg_secondary"],
                        border_color=COLORS["bg_tertiary"],
                        text_color=COLORS["white"],
                        placeholder_text_color=COLORS["white_dim"],
                        font=(FONT["family"],FONT["size_sm"]),
                        corner_radius=6,
                        border_width=1,
                )
                self.search_input.pack(fill="x")
                self.search_input.bind("<KeyRelease>", self.on_search)

                # ── FORM CONTAINER 
                # ✅ FIX Bug 1: create form_container BEFORE add_form_frame uses it as parent
                self.form_container = ctk.CTkFrame(self.frame, fg_color="transparent")
                self.form_container.pack(fill="x")
                # always packed — acts as a reserved slot above the scroll list
                # add_form_frame goes INSIDE here → no need for before= trick

                #ADD PASSWORD FROM(hidden by default):
                self.add_form_visible = False

                self.add_form_frame = ctk.CTkFrame(
                        self.form_container,
                        fg_color=COLORS["bg_secondary"],
                        corner_radius=8,
                        border_width=1,
                        border_color=COLORS["bg_tertiary"]
                )

                #FROM: ACCOUNT NAME INPUT:
                ctk.CTkLabel(
                        self.add_form_frame,
                        text="ACCOUNT NAME",
                        font=(FONT["family"],FONT["size_sm"]),
                        text_color=COLORS["blue"]
                ).pack(anchor="w", padx=14, pady=(12, 2))
                # anchor="w" → align text to left (west)

                self.account_input = ctk.CTkEntry(
                        self.add_form_frame,
                        height=34,
                        placeholder_text="e.g. Gmail, GitHub...",
                        fg_color=COLORS["bg_primary"],
                        border_color=COLORS["bg_tertiary"],
                        text_color=COLORS["white"],
                        placeholder_text_color=COLORS["white_dim"],
                        font=(FONT["family"], FONT["size_sm"]),
                        corner_radius=4,
                        border_width=1
                        )
                self.account_input.pack(fill="x", padx=14)

                #-- FROM: USERNAME INPUT:
                ctk.CTkLabel(
                        self.add_form_frame,
                        text="USERNAME / EMAIL",
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["blue"]
                ).pack(anchor="w", padx=14, pady=(8, 2))

                self.username_input = ctk.CTkEntry(
                        self.add_form_frame,
                        height=34,
                        placeholder_text="e.g. rohit@gmail.com",
                        fg_color=COLORS["bg_primary"],
                        border_color=COLORS["bg_tertiary"],
                        text_color=COLORS["white"],
                        placeholder_text_color=COLORS["white_dim"],
                        font=(FONT["family"], FONT["size_sm"]),
                        corner_radius=4,
                        border_width=1
                )
                self.username_input.pack(fill="x", padx=14)

                #FROM: PASSWORD INPUT

                ctk.CTkLabel(
                        self.add_form_frame,
                        text="PASSWORD",
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["blue"]
                ).pack(anchor="w", padx=14, pady=(8, 2))

                self.new_pass_input = ctk.CTkEntry(
                        self.add_form_frame,
                        height=34,
                        placeholder_text="enter password...",
                        show="•",
                        fg_color=COLORS["bg_primary"],
                        border_color=COLORS["bg_tertiary"],
                        text_color=COLORS["white"],
                        placeholder_text_color=COLORS["white_dim"],
                        font=(FONT["family"], FONT["size_sm"]),
                        corner_radius=4,
                        border_width=1
                )
                self.new_pass_input.pack(fill="x", padx=14)

                self.new_pass_input.bind("<KeyRelease>", self.on_password_type)
                # fires on every keystroke in password field
                # on_password_type() → updates strength meter live


                # -- STRENGTH METER 
                self.strength_label = ctk.CTkLabel(
                        self.add_form_frame,
                        text="",
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["white_dim"]
                )
                self.strength_label.pack(anchor="w", padx=14, pady=(4, 2))

                # 5 segments side by side — one per strength rule
                strength_bar_frame = ctk.CTkFrame(
                        self.add_form_frame,
                        fg_color="transparent"
                )
                strength_bar_frame.pack(fill="x", padx=14, pady=(0, 8))

                self.strength_segments = []
                # list to hold all 5 segment frames
                # we color them based on strength score

                for i in range(5):
                        # create 5 equal segments side by side
                        seg = ctk.CTkFrame(
                                strength_bar_frame,
                                height=4,
                                fg_color=COLORS["bg_tertiary"],
                                # starts as dark color = empty
                                corner_radius=2
                        )
                        seg.pack(side="left", fill="x", expand=True, padx=1)
                        # side="left" → all 5 sit in a row left to right
                        # fill="x", expand=True → each takes equal width
                        self.strength_segments.append(seg)
                        # add to list so we can color them later


        # ── FORM: ERROR + SAVE BUTTON 
                self.form_error = ctk.CTkLabel(
                        self.add_form_frame,
                        text="",
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["danger"]
                )
                self.form_error.pack(pady=(0, 4))

                ctk.CTkButton(
                        self.add_form_frame,
                        text="[ SAVE PASSWORD ]",
                        height=36,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["gold"],
                        border_width=1,
                        text_color=COLORS["gold"],
                        font=(FONT["family"], FONT["size_sm"]),
                        corner_radius=4,
                        command=self.save_password
                ).pack(fill="x", padx=14, pady=(0, 12))


        # ── SCROLLABLE PASSWORD LIST
                self.scroll_frame = ctk.CTkScrollableFrame(
                        self.frame,
                        fg_color="transparent",
                        scrollbar_button_color=COLORS["bg_tertiary"],
                        scrollbar_button_hover_color=COLORS["blue"]
                        )
                self.scroll_frame.pack(fill="both", expand=True, padx=16, pady=(6, 16))
                # fill="both", expand=True → takes all remaining space
                # CTkScrollableFrame → auto adds scrollbar when needed

                self.refresh_list()
                # load and display all passwords immediately


# ── TOGGLE ADD FORM 

        def toggle_add_form(self):
                # shows or hides the add password form
                # called when user clicks + ADD button

                self.add_form_visible = not self.add_form_visible
                # flip the boolean each time

                if self.add_form_visible:
                        self.add_form_frame.pack(fill="x", padx=16, pady=(0, 8))
                                
                                
                                
                
                else:
                        self.add_form_frame.pack_forget()
                        # pack_forget() → hides widget without destroying it
                        # widget still exists in memory — just invisible
                        self.clear_form()
                        # clear all input fields when form hides


# ── CLEAR FORM 

        def clear_form(self):
                # resets all form inputs back to empty
                self.account_input.delete(0, "end")
                self.username_input.delete(0, "end")
                self.new_pass_input.delete(0, "end")
                # delete(0, "end") → deletes from position 0 to end
                # clears entire input field

                self.strength_label.configure(text="")
                self.form_error.configure(text="")
                # reset labels back to empty

                for seg in self.strength_segments:
                        seg.configure(fg_color=COLORS["bg_tertiary"])
                # reset all 5 strength bar segments to dark color


        # ── PASSWORD STRENGTH LIVE UPDATE 

        def on_password_type(self, event):
                # called on every keystroke in password input
                # event = the key event (we don't use it directly)

                password = self.new_pass_input.get()
                # read current text in password field

                if not password:
                # if field is empty → reset everything
                        self.strength_label.configure(text="")
                        for seg in self.strength_segments:
                                seg.configure(fg_color=COLORS["bg_tertiary"])
                        return

                score, label, color = check_password_strength(password)
                # check_password_strength() returns tuple:
                # score = 0-5 (how many rules passed)
                # label = "WEAK" / "MEDIUM" / "STRONG"
                # color = hex color for the bar

                self.strength_label.configure(
                text=f"STRENGTH: {label}",
                text_color=color
                )
        # update label text and color

                for i, seg in enumerate(self.strength_segments):
                        # enumerate() → gives index AND value
                        # i = 0,1,2,3,4
                        # seg = each segment frame

                        if i < score:
                                seg.configure(fg_color=color)
                                # color segments UP TO the score
                                # score=3 → segments 0,1,2 get colored
                        else:
                                seg.configure(fg_color=COLORS["bg_tertiary"])
                                # remaining segments stay dark


        # ── SAVE PASSWORD 

        def save_password(self):
                # called when user clicks [ SAVE PASSWORD ]
                # validates inputs → encrypts → saves to JSON

                account  = self.account_input.get().strip()
                username = self.username_input.get().strip()
                password = self.new_pass_input.get().strip()

                if not account or not username or not password:
                        # check all three fields are filled
                        self.form_error.configure(text="⚠ ALL FIELDS REQUIRED")
                        return

                encrypted = encrypt_password(self.fer, password)
                # encrypt password BEFORE saving
                # crypto.py does the encryption
                # database.py receives already encrypted string

                add_password(account, username, encrypted)
                # save to vault.json
                # account and username saved as plain text
                # password saved as encrypted string

                self.toggle_add_form()
                # hide the form after saving

                self.refresh_list()
                # reload password list to show new entry


# ── SEARCH 

        def on_search(self, event):
                # called on every keystroke in search bar
                query = self.search_input.get().strip()
                self.refresh_list(query)
                # refresh list with search filter applied


# ── REFRESH PASSWORD LIST 

        def refresh_list(self, query=""):
                # clears and rebuilds the password list
                # query="" → show all passwords (no filter)
                # query="git" → show only matching passwords

                for widget in self.scroll_frame.winfo_children():
                        widget.destroy()
                        # winfo_children() → gets all widgets inside frame
                        # destroy each one → clears the list completely
                        # we rebuild from scratch every time

                passwords = search_passwords(query) if query else get_all_passwords()
                # if query exists → use search_passwords() to filter
                # if no query    → use get_all_passwords() for full list

                if not passwords:
                # show empty state message if no passwords found
                        ctk.CTkLabel(
                                self.scroll_frame,
                                text="NO PASSWORDS FOUND" if query else "NO PASSWORDS YET\nCLICK + ADD TO START",
                                font=(FONT["family"], FONT["size_md"]),
                                text_color=COLORS["white_dim"]
                        ).pack(expand=True, pady=40)
                        return

                for entry in passwords:
                        self.build_password_row(entry)
                        # build a row widget for each password entry


        # ── BUILD PASSWORD ROW 

        def build_password_row(self, entry):
                # builds one password card in the list
                # entry = one password dictionary from vault.json

                entry_id = entry["id"]

                if entry_id not in self.showing_passwords:
                        self.showing_passwords[entry_id] = False
                        # add to tracking dict if first time seeing this id
                        # False = password hidden by default


        # ── ROW CARD 
                row = ctk.CTkFrame(
                        self.scroll_frame,
                        fg_color=COLORS["bg_secondary"],
                        corner_radius=6,
                        border_width=1,
                        border_color=COLORS["bg_tertiary"]
                )
                row.pack(fill="x", pady=(0, 6))


        # ── LEFT SIDE — account info 
                left = ctk.CTkFrame(row, fg_color="transparent")
                left.pack(side="left", fill="x", expand=True, padx=12, pady=8)

                ctk.CTkLabel(
                        left,
                        text=entry["account"].upper(),
                        font=(FONT["family"], FONT["size_md"]),
                        text_color=COLORS["blue"],
                        anchor="w"
                ).pack(fill="x")

                ctk.CTkLabel(
                        left,
                        text=entry["username"],
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["white_dim"],
                        anchor="w"
                ).pack(fill="x")

        # ── PASSWORD DISPLAY 
                is_showing = self.showing_passwords[entry_id]
                # check if this password is currently visible

                if is_showing:
                        try:
                                plain = decrypt_password(self.fer, entry["password"])
                                display_text = plain
                                # decrypt and show actual password
                        except:
                                display_text = "DECRYPT ERROR"
                                # wrong master key → can't decrypt
                else:
                        display_text = "••••••••"
                        # hidden → show dots


                pass_label = ctk.CTkLabel(
                        left,
                        text=display_text,
                        font=(FONT["family"], FONT["size_sm"]),
                        text_color=COLORS["white"] if is_showing else COLORS["white_dim"],
                        anchor="w"
                )
                pass_label.pack(fill="x")


                # ── RIGHT SIDE — action buttons 
                right = ctk.CTkFrame(row, fg_color="transparent")
                right.pack(side="right", padx=8, pady=8)


        # ── SHOW/HIDE BUTTON 
                ctk.CTkButton(
                        right,
                        text="👁",
                        width=32,
                        height=32,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["bg_tertiary"],
                        border_width=1,
                        corner_radius=4,
                        command=lambda eid=entry_id: self.toggle_show_password(eid)
                        # lambda eid=entry_id → captures current entry_id
                        # without eid=entry_id → all buttons share same id (bug!)
                ).pack(pady=(0, 4))


        # ── COPY BUTTON ───────────────────────────────────────
                ctk.CTkButton(
                right,
                text="⧉",
                width=32,
                height=32,
                fg_color="transparent",
                hover_color=COLORS["bg_tertiary"],
                border_color=COLORS["gold"],
                border_width=1,
                text_color=COLORS["gold"],
                corner_radius=4,
                command=lambda e=entry: self.copy_password(e)
                ).pack(pady=(0, 4))


                # ── DELETE BUTTON ─────────────────────────────────────
                ctk.CTkButton(
                        right,
                        text="✕",
                        width=32,
                        height=32,
                        fg_color="transparent",
                        hover_color=COLORS["bg_tertiary"],
                        border_color=COLORS["danger"],
                        border_width=1,
                        text_color=COLORS["danger"],
                        corner_radius=4,
                        command=lambda eid=entry_id: self.delete_entry(eid)
                ).pack()


        # ── TOGGLE SHOW PASSWORD ──────────────────────────────────

        def toggle_show_password(self, entry_id):
                # flips show/hide state for one password entry
                self.showing_passwords[entry_id] = not self.showing_passwords[entry_id]
                # flip True → False or False → True

                query = self.search_input.get().strip()
                self.refresh_list(query)
                # refresh list to show updated state


        # ── COPY PASSWORD 

        def copy_password(self, entry):
                # copies decrypted password to clipboard
                # auto-clears clipboard after 30 seconds

                try:
                        plain = decrypt_password(self.fer, entry["password"])
                        pyperclip.copy(plain)
                        # pyperclip.copy() → puts plain password in clipboard
                        # user can now Ctrl+V anywhere

                        if self.clipboard_timer:
                                self.parent.after_cancel(self.clipboard_timer)
                                # cancel existing timer if copy clicked again
                                # resets the 30 second countdown

                        self.clipboard_timer = self.parent.after(
                                30000,
                                # 30000 milliseconds = 30 seconds
                                lambda: pyperclip.copy("")
                                # after 30s → copy empty string to clipboard
                                # clears the password from clipboard automatically
                        )

                except:
                        pass
                        # silently fail if decrypt fails


        # ── DELETE ENTRY 

        def delete_entry(self, entry_id):
                # deletes a password entry permanently
                delete_password(entry_id)
                # database.py removes entry from vault.json

                if entry_id in self.showing_passwords:
                        del self.showing_passwords[entry_id]
                        # remove from tracking dict too

                query = self.search_input.get().strip()
                self.refresh_list(query)
                # refresh list to reflect deletion


        # ── LOCK APP 

        def lock_app(self):
                # destroys dashboard and shows login screen again
                from ui.login import LoginScreen
                # import here to avoid circular imports
                # circular import = login imports dashboard
                #                   dashboard imports login = loop!

                self.frame.destroy()
                # remove dashboard completely

                def on_login_success(new_fer):
                        Dashboard(self.parent, new_fer)
                        # create fresh dashboard with new Fernet object

                LoginScreen(self.parent, on_login_success)
                # show login screen again



                











        