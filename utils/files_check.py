import os
from pathlib import Path
import json
import shutil
from tkinter import messagebox,Tk
from utils.file_handler import get_user
from utils.monthly_updater import monthly_update
from utils.date_calculator import get_today

required_directories=["data","data/users","ui","ui/assets","utils"]
required_files=["utils/file_handler.py","utils/date_calculator.py","ui/theme.py","ui/main_ui.py","ui/login.py","ui/get_preferences.py","ui/assets/dark.png","ui/assets/light.png","data/defaults.json","main.py"]

import json

def open_user_json(username):
    if not username.endswith(".json"):
        username += ".json"

    path = f"data/users/{username}"

    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {username}: {e}")
        return None   # Return None to indicate corruption

def ensure_files():
    for directory in required_directories:
        os.makedirs(directory,exist_ok=True)
    all_exist=True
    for requirment in required_files:
        file=requirment
        if Path(file).exists()==False:
            all_exist=False
    if all_exist==False:
        return False
    
def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    
def ensure_json_structure():
    files=os.listdir("data/users")
    user_files=[]
    for file in files:
        if file.endswith(".json"):
            user_files.append(file[:-5])
    with open("data/defaults.json","r") as file:
        default=json.load(file)

    # main checking/Validation
    for user in user_files:
        user_path = f"data/users/{user}.json"
        data = open_user_json(user)
        if data is None:
            # File is corrupted, backup it and create new with defaults
            backup_path = f"data/users/backup_{user}.json.bkp"
            shutil.copy(user_path, backup_path)
            root=Tk()
            messagebox.showwarning("Backup Created",f"Backed up corrupted {user}.json to {backup_path}")
            root.destroy()
            data = default.copy()  # Use defaults
        else:
            # Process as before
            for key, value in default.items():
                # 1. Missing key
                if key not in data:
                    data[key] = value

                else:
                    # 2. Type check
                    if type(data[key]) != type(value):
                        data[key] = value

                    # 3. Empty value check
                    elif data[key] in [None, "", " ", [], {}]:
                        data[key] = value

                    # 4. Nested dict check
                    elif isinstance(value, dict):
                        for sub_key, sub_val in value.items():
                            if sub_key not in data[key]:
                                data[key][sub_key] = sub_val
        write_json(user_path, data)
        #Credits for this func: ChatGPT(missing data filled),GithubCopilot (corrupted files data loss prevention)

def ensure_user_months():
    users=get_user()
    current_month=get_today().strftime("%Y-%m")  # Compare full YYYY-MM format
    for user in users:
        data=open_user_json(user)
        month=str(data["budget"]["month"])
        if month!=current_month:  # Compare full month string
            print(f"Updating {user}: {month} -> {current_month}")
            monthly_update(user)
        
ensure_json_structure()
ensure_user_months()