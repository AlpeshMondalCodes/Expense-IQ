import customtkinter as ctk
from tkinter import ttk,messagebox
from PIL import Image
import json
from ui.theme import *
from ui.login import login_window
from ui.main_ui import main_ui
from utils.file_handler import check_pass,get_remember_default,open_user_json
from utils.files_check import ensure_files

def on_login(username,window,theme,remember):
    pass_dia=ctk.CTkInputDialog(text="Password")
    entered_password=pass_dia.get_input()
    logged_in=check_pass(username,entered_password)
    if logged_in:
        window.unbind_all("<Escape>")
        window.withdraw()
        main_ui(username,theme,window,remember)
    else:
        return False

app_data=get_remember_default()

def login_remembered_user():
    username=app_data["username"]
    theme=open_user_json(username)["settings"]["theme"]
    window=None
    main_ui(username,theme,window,1)

if app_data["remember"]==1:
    login_remembered_user()
    if ensure_files()==False:
        messagebox.showerror("No File Exists","Some of the required files are missing")
        quit()
else:
    login_window(on_login)
    if ensure_files()==False:
        messagebox.showerror("No File Exists","Some of the required files are missing")
        quit()