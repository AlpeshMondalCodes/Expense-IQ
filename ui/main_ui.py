import customtkinter as ctk
from ui.new_transaction import new_transaction
from ui.theme import *
from utils.file_handler import read_json,write_json,update_password,reset_userdata,delete,open_user_json,get_remember_default,forgot_user
from utils.date_calculator import *
from tkinter import messagebox
from tkinter.ttk import Treeview

def clear_content(frame):
    for widget in frame.winfo_children():
        widget.destroy()

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
    alert_btn=ctk.CTkButton(topbar,text="Alerts",font=("Calbri",14),fg_color=DARK["card"],corner_radius=10,hover_color=DANGER)
    alert_btn.pack(side="right",padx=20,pady=5,ipady=5)
    left_frame = ctk.CTkFrame(topbar, fg_color="transparent")
    left_frame.pack(side="left", padx=10)
    welcome_lbl=ctk.CTkLabel(left_frame,text=name_str,fg_color=DARK["card"],font=("Arial",16,"bold"),corner_radius=10)
    balance_lbl=ctk.CTkLabel(left_frame,text=balance_str,fg_color=DARK["card"],font=("Arial",20),corner_radius=10)


    welcome_lbl.pack( side="left",ipady=5)
    balance_lbl.pack( side="left", padx=10,ipady=5)

def Dashboard(content_frame,username):
    clear_content(content_frame)
    expense_frame=ctk.CTkFrame(content_frame,fg_color=DARK["frame"])
    expense_frame.place(relwidth=0.475,relheight=0.475,relx=0.025,y=20)
    ctk.CTkLabel(expense_frame,text="Expense Frame",fg_color="red").pack(expand=True,fill="both")

    budget_progressbar_frame=ctk.CTkFrame(content_frame,fg_color=DARK["frame"])
    budget_progressbar_frame.place(relwidth=0.475,relheight=0.475,relx=0.5,y=20)
    ctk.CTkLabel(budget_progressbar_frame,text="Progressbar Frame",fg_color="green").pack(expand=True,fill="both")

    transaction_frame=ctk.CTkFrame(content_frame,fg_color=DARK["frame"])
    transaction_frame.place(relwidth=0.95,relheight=0.475,relx=0.025,rely=0.5)
    user_json=open_user_json(username)
    transactions=user_json["data"]["transactions"]
    if transactions==[{}] or not transactions or all(not t for t in transactions):
        ctk.CTkLabel(transaction_frame,text="No Transactions").place(anchor="center",relx=0.5,rely=0.5)
    
def transactions_tab(content_frame,user):
    clear_content(content_frame)
    data=open_user_json(user)
    transactions=data["data"]["transactions"]
    
    if not transactions or (len(transactions) == 1 and not transactions[0]):
        ctk.CTkLabel(content_frame,text="No Transactions").pack()
    else:

        rows = len(transactions)
        table_frame=ctk.CTkScrollableFrame(content_frame,fg_color=DARK["card"])
        table_frame.pack(expand=True,fill="both")
        table_frame.rowconfigure(rows,uniform="a")
        table_frame.columnconfigure(0,weight=1,uniform="a")

        selected=[None,None]

        def hover_item(e):
            e.configure(fg_color=DARK["card_hover"])

        def unhover_item(e):
            e.configure(fg_color="transparent")

        def select_item(e,ID):
            nonlocal selected
            if selected[0]==None:
                selected[0]=e
                selected[1]=ID
            else:
                selected[0].configure(border_color=DARK["card"])
                selected[0]=e
                selected[1]=ID
            e.configure(border_color=PRIMARY)

        # Table generation -------------------------------------------------------------------------------------------------------------
        row_frame=[]
        for i in range(rows):
            txn = transactions[i]
            if txn["type"]=="Expense":
                color=LOSS_COLOR
            else:
                color=GAIN_COLOR

            row_frame.append(ctk.CTkFrame(table_frame,fg_color="transparent",border_width=1,border_color=DARK["card"])) #???? why append i should have used [i]=ctk.Frmae() ? "reason(main_ui.py - line 80).png"
            row_frame[i].grid(row=i, column=0,columnspan=4, sticky="ew", padx=5, pady=5)

            row_frame[i].columnconfigure(0,weight=1,uniform="a")
            row_frame[i].columnconfigure(1,weight=4,uniform="a")
            row_frame[i].columnconfigure(2,weight=3,uniform="a")
            row_frame[i].columnconfigure(3,weight=2,uniform="a")
            row_frame[i].columnconfigure(4,weight=3,uniform="a")
            ctk.CTkLabel(row_frame[i], text=txn["id"]).grid(row=0, column=0, padx=5, pady=5)
            ctk.CTkLabel(row_frame[i], text=txn["title"]).grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(row_frame[i], text=txn["amount"],text_color=color).grid(row=0, column=2, padx=5, pady=5)
            ctk.CTkLabel(row_frame[i], text=txn["date"]).grid(row=0, column=3, padx=5, pady=5)
            ctk.CTkLabel(row_frame[i], text=txn["category"]).grid(row=0, column=4, padx=5, pady=5)

            row_frame[i].bind("<Enter>", lambda e,index=i: hover_item(row_frame[index]))
            row_frame[i].bind("<Button-1>", lambda e,index=i,ID=txn["id"]: select_item(row_frame[index],ID))
            row_frame[i].bind("<Leave>", lambda e,index=i: unhover_item(row_frame[index]))

            for child in row_frame[i].winfo_children():
                child.bind("<Enter>", lambda e,index=i: hover_item(row_frame[index]))
                child.bind("<Button-1>", lambda e,index=i,ID=txn["id"]: select_item(row_frame[index],ID))
                child.bind("<Leave>", lambda e,index=i: unhover_item(row_frame[index]))

        def delete_transaction(user):
            uid=selected[1]
            deleted_amount=0
            deleted_expense=True
            
            # Find and remove transaction
            for txn in transactions[:]:
                if txn["id"]==uid:
                    deleted_amount=txn["amount"]
                    deleted_expense=txn["type"]=="Expense"
                    transactions.remove(txn)
                    break
            
            # Renumber all IDs
            for i in range(len(transactions)):
                transactions[i]["id"]=i+1

            #updating userFile
            data=open_user_json(user)                
            data["data"]["transactions"]=transactions
            if deleted_expense:
                data["data"]["balance"]+=deleted_amount
                data["budget"]["current_spent"]-=deleted_amount
                data["analytics"]["monthly_summary"]["Expense"]-=deleted_amount
            if not deleted_expense:
                data["data"]["balance"]-=deleted_amount
                data["analytics"]["monthly_summary"]["income"]-=deleted_amount
            write_json(f"data/users/{user}.json",data)

            messagebox.showinfo("Deleted",f"Transaction Deleted successfully\nid:{uid}")
            transactions_tab(content_frame,user)


        del_btn=ctk.CTkButton(content_frame,text="Delete ⮾",width=150,height=45,corner_radius=10,fg_color=DANGER,hover_color=WARNING,bg_color=DARK["card"],text_color=DARK["border"],command=lambda: delete_transaction(user))
        del_btn.place(rely=1,relx=0.8,x=-50,y=-10,anchor="se")

    new_btn=ctk.CTkButton(content_frame,text="New Transaction",width=200,height=45,corner_radius=10,fg_color=SUCCESS,hover_color=WARNING,bg_color=DARK["card"],text_color=DARK["border"],command=lambda :new_transaction(user,Dashboard,content_frame))
    new_btn.place(rely=1,relx=1,x=-45,y=-10,anchor="se")
    
def budget_tab(content_frame,username):
    clear_content(content_frame)
    data=open_user_json(username)
    budget_data=data["budget"]
    monthly_income=data["data"]["monthly_income"]
    balance=data["data"]["balance"]
    monthly_limit=budget_data["monthly_limit"]
    spent=budget_data["current_spent"]
    currency=data["profile"]["currency"]
    saving=data["analytics"]["monthly_summary"]["savings"]

    frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    frame.pack(side="left", padx=10, pady=10,fill="x",anchor="nw")

    # budget coloring
    if spent > monthly_limit:
        spent_color = DANGER
    elif spent > monthly_limit * 0.7:
        spent_color = WARNING
    else:
        spent_color = SUCCESS

    title=ctk.CTkLabel(frame,text_color=DARK["text"],text="Monthly Overveiw",font=("Arial",24,"bold"))
    budget=ctk.CTkLabel(frame,text_color=DARK["subtext"],text=f"Monthly Budget:{currency} {monthly_limit}",font=("Arial",20))
    income=ctk.CTkLabel(frame,text_color=DARK["subtext"],text=f"Monthly Income:{currency} {monthly_income}",font=("Arial",20))
    spent_title=ctk.CTkLabel(frame,text=f"Monthly Spent:{currency} {spent}",font=("Arial",20),text_color=spent_color)
    balance_lbl=ctk.CTkLabel(frame,text_color=DARK["subtext"],text=f"Monthly Balance:{currency} {balance}",font=("Arial",20))

    frame2=ctk.CTkFrame(content_frame, fg_color="transparent")
    frame2.pack(padx=10, pady=10,fill="both",expand=True,side="right",anchor="ne")

    #progress
    expense_progress=ctk.CTkProgressBar(frame2,corner_radius=5,progress_color=spent_color,fg_color=DARK["bg"])
    expense_progress.set(spent/monthly_limit)

    saving_lbl=ctk.CTkLabel(frame2,text=f"Savings:{currency} {saving}",corner_radius=10,fg_color=DARK["card"])

    #layout
    title.pack(pady=15,padx=10)
    budget.pack(pady=15,padx=10)
    spent_title.pack(pady=15,padx=10)
    balance_lbl.pack(pady=15,padx=10)

    expense_progress.pack(anchor="n",ipadx=5,ipady=5,padx=10,pady=10,fill="x")
    saving_lbl.pack(anchor="n",ipadx=5,ipady=5,padx=10,pady=10)

    
    

def setting(content_frame, username, current_theme="dark"):
    clear_content(content_frame)
    data = read_json(f"data/users/{username}.json")

    # Select theme dict
    THEME = DARK if current_theme == "dark" else LIGHT

    # ===== Container Card =====
    top_left_card=ctk.CTkFrame(content_frame,bg_color="transparent",fg_color="transparent")
    top_left_card.pack(anchor="nw")

    theme_card = ctk.CTkFrame(top_left_card,fg_color=THEME["card"],corner_radius=15,border_width=2,border_color=THEME["border"])
    theme_card.pack(side="left",padx=30, pady=30,anchor="nw")

    # ===== Title =====
    title = ctk.CTkLabel(theme_card,text="Appearance",font=("Segoe UI", 26, "bold"),text_color=THEME["text"])
    title.pack(anchor="w", padx=20, pady=(15, 5))
    subtitle = ctk.CTkLabel(theme_card,text="Choose your theme",font=("Segoe UI", 16),text_color=THEME["subtext"])
    subtitle.pack(anchor="w", padx=20, pady=(0, 15))

    theme_var = ctk.StringVar()

    def update_var(value):
        # print("Theme:", value)
        data["settings"]["theme"] = value
        write_json(f"data/users/{username}.json", data)

    # ===== Segmented Button (BIG + Styled) =====
    themeToggle = ctk.CTkSegmentedButton(
        theme_card,
        values=["dark", "light"],
        variable=theme_var,
        command=update_var,

        # Styling
        width=300,
        height=45,
        corner_radius=10,

        fg_color=THEME["frame"],
        selected_color=THEME["primary"],
        selected_hover_color=THEME["primary_hover"],
        unselected_color=THEME["card"],
        text_color=THEME["text"],
        font=("Segoe UI", 16, "bold")
    )
    themeToggle.pack(padx=20, pady=(0, 20))

    # ===== Set Default =====
    current = data.get("settings", {}).get("theme", "dark")
    themeToggle.set(current)

    #-------------------------------------------------------------------------------------------------------------------

    currency_card = ctk.CTkFrame(top_left_card,fg_color=THEME["card"],corner_radius=15,border_width=2,border_color=THEME["border"])
    currency_card.pack(side="left",padx=(0,30), pady=30,anchor="nw")
    # ===== Title =====
    title2 = ctk.CTkLabel(currency_card,text="Currency",font=("Segoe UI", 26, "bold"),text_color=THEME["text"])
    title2.pack(anchor="w", padx=20, pady=(15, 5))
    subtitle2 = ctk.CTkLabel(currency_card,text="Choose your Currency",font=("Segoe UI", 16),text_color=THEME["subtext"])
    subtitle2.pack(anchor="w", padx=20, pady=(0, 15))

    def SwitchCurrency(value):
        data["profile"]["currency"]=value
        write_json(f"data/users/{username}.json",data)

    currency_menu=ctk.CTkOptionMenu(
        currency_card,
        values=["USD","INR","EUR","GBP"],
        command=SwitchCurrency,
        # Styling
        width=300,
        height=45,
        corner_radius=10,

        fg_color=THEME["frame"],
        text_color=THEME["text"],
        dropdown_fg_color=THEME["frame"],
        button_color=THEME["primary"],
        button_hover_color=THEME["primary_hover"],
        dropdown_hover_color=THEME["card"],
        font=("Segoe UI", 16, "bold")
    )
    currency_menu.pack(padx=20, pady=(0, 20))

    currency_menu.set(data["profile"]["currency"])

    #------------------------------------------------------------------------------------------------------------------------------------------------------
    password_Frame=ctk.CTkFrame(content_frame,bg_color="transparent",fg_color="transparent")
    password_Frame.pack(anchor="nw",padx=30)
    password_card = ctk.CTkFrame(password_Frame,fg_color=THEME["card"],corner_radius=15,border_width=2,border_color=THEME["border"])
    password_card.pack(side="left",padx=(0,30), pady=30,anchor="nw")
    # ===== Title =====
    title3 = ctk.CTkLabel(password_card,text="Change Password",font=("Segoe UI", 26, "bold"),text_color=THEME["text"])
    title3.pack(anchor="w", padx=20, pady=(15, 5))
    subtitle3 = ctk.CTkLabel(password_card,text="Enter your new password",font=("Segoe UI", 16),text_color=THEME["subtext"])
    subtitle3.pack(anchor="w", padx=20, pady=(0, 15))

    passEntry=ctk.CTkEntry(
        password_card,
        width=300,
        height=45,
        corner_radius=10,

        fg_color=THEME["card"],
        border_color=PRIMARY,
        placeholder_text_color=THEME["subtext"],
        text_color=THEME["text"],
        placeholder_text=data["auth"]["password"],
        font=("Segoe UI", 16, "bold")
    )
    update_btn=ctk.CTkButton(
        password_card,
        text="UPDATE",
        command=lambda:update_password(username,passEntry.get()),
        width=300,
        height=45,
        corner_radius=10,

        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        border_color=YELLOW_BORDER,
        text_color=THEME["text"]
    )

    passEntry.pack(padx=20, pady=(0, 20))
    update_btn.pack(padx=20, pady=(0, 20))

    # _____________________________________________________________________________________________________________________________________________

    button_frame=ctk.CTkFrame(content_frame,fg_color="transparent")
    button_frame.place(relx=1,rely=0,x=-30,y=30,anchor="ne")

    def reset():
        status=messagebox.askyesno(title="Are you sure?",message="All your transaction histories and customizations will be removed and cannot be recovered.\nAre you sure you want to reset your data?\nNote:The 5 preferences asked at account creation will not be cleared.")
        if status:
            reset_userdata(username)
            msg="All data of your account cleared except authentication data,profile(includes name and currency),monthly limit,threshold percent, and your theme preference\nTodelete your account you can click on Delete Account button in the Settings tab."
            messagebox.showinfo("Deletion Completed",msg)

    reset_btn=ctk.CTkButton(
        button_frame,
        text="RESET",
        command=reset,
        width=150,
        height=45,
        corner_radius=10,

        fg_color=DANGER,
        hover_color="red",
        border_color=RED_BORDER,
        text_color=THEME["text"]
    )
    reset_btn.pack(pady=10)

    def deletion():
        status=messagebox.askyesno("Are you sure?","This action will delete all your data and it is not recoverable.\nWould you like to proceed?")
        if status:
            delete(username)
            quit()

    delete_btn=ctk.CTkButton(
        button_frame,
        text="DELETE",
        command=deletion,
        width=150,
        height=45,
        corner_radius=10,

        fg_color="#b23930",
        hover_color="red",
        border_color=DANGER,
        text_color=THEME["text"]
    )
    delete_btn.pack(pady=10)

    def forgot():
        forgot_user()
        messagebox.showinfo("Done","Now the user will not be automatically logged in")
        forgot_btn.configure(state="disabled")

    forgot_btn=ctk.CTkButton(button_frame,text_color="#000000",text="Show Login Window",width=150,height=45,corner_radius=10,fg_color=WARNING,hover_color="orange",border_color=YELLOW_BORDER,command=forgot)
    forgot_btn.pack(pady=10)

    if get_remember_default()["remember"]==1:
        forgot_btn.configure(state="enabled")
    else:
        forgot_btn.configure(state="disabled")


    #########################################################################################################################################################3

def main_ui(username,theme,login,remember):
    ###3 remember me feat
    data=get_remember_default()
    data["remember"]=remember
    if remember:
        data["username"]=username
    else:
        data["username"]=""
    write_json("data/app.json",data)
################################################################3
    try:
        login.destroy()
    except:
        pass

    root=ctk.CTk()
    root.title("Expense IQ: Expend Conciously")
    root.configure(fg_color=(LIGHT["bg"],DARK["bg"]))
    root.minsize(1200,560)
    

    centered_window(root,1280,720)
    root._set_appearance_mode(theme)
    ####### SIDEBAR ######################################################################################
    sidebar=ctk.CTkFrame(root,width=200,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)
    #------ SIDEBAR BUTTONS ------------------------------------------------------------------------------
    today=ctk.CTkLabel(sidebar,text=str(get_today()),font=("Segoe UI",20,"bold"),fg_color="transparent")
    day=ctk.CTkLabel(sidebar,text=str(get_weekday_formatted()),font=("Segoe UI",14,"bold"),fg_color="transparent")
    dashboard=ctk.CTkButton(sidebar,text="Dashboard",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DARK["border"],corner_radius=10,border_color=PRIMARY_HOVER,border_width=1,height=45,command=lambda:Dashboard(content_frame,username))
    transaction=ctk.CTkButton(sidebar,text="Transaction",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DARK["border"],corner_radius=10,border_color=PRIMARY_HOVER,border_width=1,height=45,command=lambda:transactions_tab(content_frame,username))
    budget=ctk.CTkButton(sidebar,text="Budget",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DARK["border"],corner_radius=10,border_color=PRIMARY_HOVER,border_width=1,height=45,command=lambda:budget_tab(content_frame,username))
    analytics=ctk.CTkButton(sidebar,text="Analytics",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DARK["border"],corner_radius=10,border_color=PRIMARY_HOVER,border_width=1,height=45)
    settings=ctk.CTkButton(sidebar,text="Settings",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DARK["border"],corner_radius=10,border_color=PRIMARY_HOVER,border_width=1,height=45,command=lambda:setting(content_frame,username))
    logout=ctk.CTkButton(sidebar,text="Logout",font=("Segoe UI Semibold",24),fg_color=DARK["card"],hover_color=DANGER,corner_radius=10,border_color=RED_BORDER,border_width=1,height=45,command=lambda:[root.quit(),root.after(10,quit())]) # used quit instead of destroy to quit safely

    today.pack(pady=(15,0),padx=10,fill="x")
    day.pack(pady=(0,15),padx=10,fill="x")
    dashboard.pack(pady=10,padx=10,fill="x")
    transaction.pack(pady=10,padx=10,fill="x")
    budget.pack(pady=10,padx=10,fill="x")
    analytics.pack(pady=10,padx=10,fill="x")
    logout.pack(pady=10,padx=10,fill="x",side="bottom")
    settings.pack(pady=10,padx=10,fill="x",side="bottom")
    #################################################################################################
    topbar=ctk.CTkFrame(root,height=50,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    topbar.pack(side="top",fill="x")
    topbar.pack_propagate(False)

    fill_topbar(username,topbar)

    content_frame=ctk.CTkFrame(root,border_color=BLUE_BORDER,fg_color=(LIGHT["frame"],DARK["frame"]))
    content_frame.pack(expand=True,fill="both",padx=20,pady=20)

    Dashboard(content_frame,username)

    root.mainloop()
