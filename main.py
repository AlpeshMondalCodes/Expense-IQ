import customtkinter as ctk
from tkinter import ttk
from PIL import Image
import json
from ui.theme import *
from ui.login import login_window
from ui.main_ui import main_ui
from utils.file_handler import check_pass

def on_login(username,window,theme):
    print("Main got:",username)
    pass_dia=ctk.CTkInputDialog(text="Password")
    entered_password=pass_dia.get_input()
    logged_in=check_pass(username,entered_password)
    if logged_in:
        window.unbind_all("<Escape>")
        window.withdraw()
        main_ui(username,theme,window)

login_window(on_login)