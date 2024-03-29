import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import login.logindb as logindb
import home.Homepage as Homepage
import logger as lu

entry_password = None
entry_username = None
login_frame = None


def check_login():
    global login_frame
    global current_user
    username = entry_username.get()
    password = entry_password.get()

    if logindb.check_credentials(username, password):
        messagebox.showinfo("Successful", "Login Successful!")
        current_user = username
        lu.log_activity(username, "LOG-IN")
        Homepage.open_homepage(login_frame)
    else:
        messagebox.showerror("Error", "Wrong Username  Or Password.")


def initloginpage(prev_main_frame):
    prev_main_frame.destroy()
    global entry_username, entry_password, login_frame

    login_destroyer()

    login_frame = tk.Frame(prev_main_frame.master)
    login_frame.pack(expand=True)

    style = ttk.Style()

    # Use the 'radiance' theme
    style.theme_use('radiance')

    label_heading = ttk.Label(
        login_frame, text="Malkhana Management System", font=("Verdana", 30))
    label_heading.grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky=tk.W)

    prev_main_frame.master.title("Login Page")
    logindb.initialize_db()

    label_username = ttk.Label(
        login_frame, text="User ID:", font=("Helvetica", 12))
    label_password = ttk.Label(
        login_frame, text="Password", font=("Helvetica", 12))
    entry_username = ttk.Entry(login_frame, font=("Helvetica", 12))
    entry_password = ttk.Entry(login_frame, show="*", font=("Helvetica", 12))
    button_login = tk.Button(login_frame, text="Enter",
                             background=style.lookup('TButton', 'background'),
                             command=check_login, font=("Helvetica", 12))

    label_username.grid(row=2, column=0, pady=10, sticky=tk.W)
    entry_username.grid(row=2, column=1, pady=5, sticky=tk.EW)
    label_password.grid(row=3, column=0, pady=10, sticky=tk.W)
    entry_password.grid(row=3, column=1, pady=5, sticky=tk.EW)
    button_login.grid(row=4, column=0, columnspan=2, pady=20, sticky=tk.EW)


def login_destroyer():
    if login_frame is not None:
        login_frame.destroy()
