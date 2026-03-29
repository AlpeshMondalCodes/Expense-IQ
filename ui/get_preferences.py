import customtkinter as ctk


# ---------------- COLORS ----------------
BG = "#181825"
SURFACE = "#1e1e2e"
TEXT = "#cdd6f4"
SUBTEXT = "#a6adc8"
ACCENT = "#5865F2"       # blurple
ACCENT_HOVER = "#4752C4" # darker hover
ACCENT_PRESSED = "#3c45a5"
GREEN = "#a6e3a1"
BORDER = "#7f849c"
DANGER  = "#f38ba8"


def centered_window(parent, width, height):
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - height // 2
    parent.geometry(f"{width}x{height}+{x}+{y}")


def get_preferences(parent):
    pref=None
    ctk.set_appearance_mode("dark")
    window = ctk.CTkToplevel(parent)
    window.title("Provide Data for your Account")
    centered_window(window, 1000, 400)
    window.resizable(False, False)
    window.configure(fg_color=BG)

    questions=["What should we call you?","Set your monthly spending budget","Warn me when spending reaches ___ %","Which currency do you follow","What is your theme preference"]
    data={
        "name":"",
        "monthly_limit":0,
        "threshold_percent":0,
        "currency":"",
        "theme":""
    }
    keys=["name","monthly_limit","threshold_percent","currency","theme"]
    current_index=0


    def ask_choices():
        global options, next_btn2
        nonlocal current_index, pref

        ans = options.get()
        data[keys[current_index]] = ans

        if current_index == 4:
            pref = data
            progress_data.set((current_index + 1) / 5)
            window.after(100, window.destroy)
            return

        current_index += 1
        title.configure(text=questions[current_index])

        options.configure(values=values[current_index - 3])

        progress_data.set((current_index + 1) / 5)

        if current_index == 3:
            options.set("INR")
        else:
            options.set("Dark")

        if current_index == 4:
            next_btn2.configure(text="Finish")

            



    def init_choices():
        nonlocal current_index,questions
        global options,next_btn2
        #theming local colors
        SURFACE = "#313244"   # menu background
        OVERLAY = "#45475A"   # hover
        TEXT = "#CDD6F4"      # text
        current_index+=1
        progress_data.set((current_index + 1) / 5)
        entry.destroy()
        next_btn.destroy()
        title.configure(text=questions[current_index])
        options = ctk.CTkOptionMenu(dataFrame,fg_color=SURFACE,button_color=ACCENT,button_hover_color=OVERLAY,dropdown_fg_color=SURFACE,dropdown_hover_color=OVERLAY,dropdown_text_color=TEXT,text_color=TEXT,font=("Segoe UI", 22),width=500,height=50,corner_radius=10)
        options.pack(pady=10)
        options.configure(values=values[0])
        options.set("INR")
        next_btn2 = ctk.CTkButton(dataFrame,text="Next",fg_color="#454FBF",hover_color="#5865F2",text_color="white",font=("Segoe UI Semibold", 18),width=140,height=45,corner_radius=8,border_width=1,border_color="#6c78ff",command=ask_choices)
        next_btn2.pack(pady=20)



    

    def go_next():
        nonlocal current_index
        answer=entry.get()
        if answer!="" and answer!=" " and current_index==0:
            data[keys[current_index]]=answer
        elif answer!="" and answer!=" " and current_index>0:
            try:
                number=int(answer)
            except ValueError:
                title.configure(text="Provide a number",text_color=DANGER)
                window.after(2000,lambda: title.configure(text=questions[current_index],text_color=TEXT))
                return
        else:
            title.configure(text="Don't leave the entry field empty")

            window.after(2000,lambda: title.configure(text=questions[current_index]))
            return
        
        if current_index<2:
            title.configure(text=questions[current_index+1])
            entry.delete(0,len(questions[current_index+1]))
            progress_data.set((current_index+2)/5)
            current_index+=1
        else:
            init_choices()

    # Top heading
    ctk.CTkLabel(window,text="Give Required Data",font=("Bahnschrift SemiBold", 36, "bold"),text_color=TEXT).pack(pady=(20, 10))

    # Main frame
    dataFrame = ctk.CTkFrame(window,fg_color=SURFACE,corner_radius=16)
    dataFrame.pack(expand=True, fill="both", padx=20, pady=10)

    # Progress bar
    progress_data = ctk.DoubleVar(value=1/5)
    progress = ctk.CTkProgressBar(dataFrame,variable=progress_data,progress_color=GREEN,fg_color="#313244",height=12)
    progress.pack(side="top", fill="x", padx=25, pady=20)

    # Question title
    title = ctk.CTkLabel(dataFrame,text=questions[current_index],font=("Segoe UI Semibold", 28, "bold"),text_color=TEXT)
    title.pack(pady=15)

    # Input field
    entry = ctk.CTkEntry(dataFrame,fg_color=BG,border_color=ACCENT,text_color=TEXT,font=("Segoe UI", 22),width=500,height=50,corner_radius=10)
    entry.pack(pady=10)


    values=[["USD","INR","EUR","GBP"],
            ["Dark","Light"]]

    # Next button
    next_btn = ctk.CTkButton(dataFrame,text="Next",fg_color="#454FBF",hover_color="#5865F2",text_color="white",font=("Segoe UI Semibold", 18),width=140,height=45,corner_radius=8,border_width=1,border_color="#6c78ff",command=go_next)
    next_btn.pack(pady=20)


    parent.wait_window(window)
    return pref

#prefer rewriting newer logic using correctindex and if to control widgets inside one single func