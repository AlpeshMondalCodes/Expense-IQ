import customtkinter as ctk
from ui.theme import *
from utils.file_handler import read_json

def centered_window(parent,width,height):
    screen_width=parent.winfo_screenwidth()
    screen_height=parent.winfo_screenheight()
    x=screen_width//2-width//2
    y=screen_height//2-height//2
    parent.geometry(f"{width}x{height}+{x}+{y}")

def fill_topbar(username,topbar):
    global balance_lbl,welcome_lbl

    data=read_json(f"data/users/{username}.json")
    name=data["profile"]["name"]
    name_str=f" Welcome {str(name)} "
    balance=data["data"]["balance"]
    balance_str=f" Current Balance:{int(balance)} "
    alert_btn=ctk.CTkButton(topbar,text="Alerts",fg_color=DARK["card"],corner_radius=10,hover_color=DANGER)
    alert_btn.pack(side="right",padx=20,pady=5,ipady=5)
    left_frame = ctk.CTkFrame(topbar, fg_color="transparent")
    left_frame.pack(side="left", padx=10)
    welcome_lbl=ctk.CTkLabel(left_frame,text=name_str,fg_color=DARK["card"],font=("Arial",16,"bold"),corner_radius=10)
    balance_lbl=ctk.CTkLabel(left_frame,text=balance_str,fg_color=DARK["card"],font=("Arial",20),corner_radius=10)


    welcome_lbl.pack( side="left")
    balance_lbl.pack( side="left", padx=10)

def main_ui(username,theme,login):
    try:
        login.destroy()
    except:
        pass

    root=ctk.CTk()
    root.title("Expense IQ: Expend Conciously")
    root.configure(fg_color=(LIGHT["bg"],DARK["bg"]))
    root.minsize(1000,560)
    

    centered_window(root,1280,720)
    root._set_appearance_mode(theme)
    sidebar=ctk.CTkFrame(root,width=200,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)
    lbl=ctk.CTkLabel(sidebar,text="Sidebar",fg_color="red")
    lbl.pack(expand=True,fill="both")

    topbar=ctk.CTkFrame(root,height=50,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    topbar.pack(side="top",fill="x")
    topbar.pack_propagate(False)

    fill_topbar(username,topbar)

    content_frame=ctk.CTkFrame(root,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    content_frame.pack(expand=True,fill="both",padx=20,pady=20)

    lbl=ctk.CTkLabel(content_frame,text="Content Frame",fg_color="blue")
    lbl.pack(expand=True,fill="both")

    root.mainloop()
