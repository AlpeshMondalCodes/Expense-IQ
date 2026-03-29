import json
import os
from ui.theme import *

def get_user():
    usernames=os.listdir("data/users")
    users=[]
    for sorting in usernames:
        if sorting.endswith(".json"):
            users.append((sorting[:-5]))
    return users

import json

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def open_user_json(username):
    if username.endswith(".json"):
        try:
            with open(f"data/users/{username}","r")as file:
                data=json.load(file)
        except Exception as e:
            data=str(e)
    else:
        try:
            with open(f"data/users/{username}.json") as file:
                data=json.load(file)
        except Exception as e:
            data=str(e)
    return data

def check_pass(username,user_pass):
    data=open_user_json(username)
    auth=data["auth"]
    if user_pass==auth["password"]:
        logged_in=True
    else:
        logged_in=False
    return logged_in

def check_user_exist(username_entry):
    entered_name=username_entry.get()
    users=get_user()
    if entered_name in users:
        available_space=False
        border=DARK["primary"]
    else:
        available_space=True
        border=GREEN_BORDER
    #handling placeholder text "Username"
    if entered_name== "Username":
        border=DARK["primary"]
        username_entry.configure(border_color=border)
        return

    username_entry.configure(border_color=border)
    
def signupUser(username,password,parent):
    from tkinter import messagebox
    from ui.get_preferences import get_preferences
    data=read_json("data/defaults.json")
    auth=data.get("auth",{"username":"",
                          "password":""})
    auth["username"]=username
    auth["password"]=password
    data["auth"]=auth
    profile=data.get("profile",{"name":"",
                                "currency":""})
    profile["name"]=username

    pref=get_preferences(parent)
    try:
        data["profile"]["name"]=pref.get("name","")
        data["profile"]["currency"]=pref.get("currency","")
        data["budget"]["monthly_limit"]=int(pref.get("monthly_limit",0))
        data["budget"]["threshold_percent"]=int(pref.get("threshold_percent",0))
        data["settings"]["theme"]=pref.get("theme","dark")
    except AttributeError:
        messagebox.showerror("Closed","The Application has been closed by the user without submitting data\nRestart")
        parent.quit()
        parent.destroy()
        return
    write_json(f"data/users/{username}.json",data)
    return True



    