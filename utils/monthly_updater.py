from datetime import date
from utils.file_handler import open_user_json,write_json,save_transaction,read_json
def monthly_update(user,month=None):
    today=date.today()
    data=open_user_json(user)
    monthy_income=data["data"]["monthly_income"]
    
    # Save salary transaction first
    save_transaction(user,"Monthly Salary Creditted",monthy_income,"Income","Salary")
    
    # Reload data to get updated balance and analytics from save_transaction
    data=open_user_json(user)
    
    # Reset analytics to only show current month's data
    data["analytics"]={
        "monthly_summary": {
                "income": monthy_income,
                "Expense": 0,
                "savings": 0
            }
    }
    data["budget"]["current_spent"]=0
    if month==None:
        data["budget"]["month"]=today.strftime("%Y-%m")
    else:
        data["budget"]["month"]=month
    write_json(f"data/users/{user}.json",data)

    appData=read_json("data/app.json")
    if int(appData["month_processed"])!=int(today.strftime("%m")):
        appData["month_processed"]=today.strftime("%m")
        write_json("data/app.json",appData)