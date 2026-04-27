import customtkinter as ctk 
from  theme import COLORS , FONT
from ui.login import LoginScreen
from ui.dashbord import Dashboard

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# WINDOW SETUP

app = ctk.CTk()             #ctk.CTk() → creates the main application window,everything else (buttons, labels, inputs) goes INSIDE this
app.title("password Vault")     #sets the text shown in the title bar at the top of the window / see "Password Vault" in the taskbar too
app.geometry("420x560")
app.resizable(False,False)              # first  False → cannot resize horizontally (width locked) / second False → cannot resize vertically (height locked)
app.configure(fg_color=COLORS["bg_primary"])       # fg_color = foreground color (background of the window itself)

def on_login_success(fer):
    Dashboard(app,fer)
    # create dashboard passing:
    # app → the main window
    # fer → the Fernet encryption object

# create the login screen
# pass app as parent → pass on_login_success as callback
LoginScreen(app, on_login_success)

app.mainloop()


































