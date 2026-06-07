from datetime import date
import datetime
from time import *

def get_today():
    return date.today()

def get_weekday_formatted():
    day=date.weekday(date.today())
    if day==0:
        txt="M  O  N"
    if day==1:
        txt="T  U  E"
    if day==2:
        txt="W  E  D"
    if day==3:
        txt="T  H  U"
    if day==4:
        txt="F  R  I"
    if day==5:
        txt="S  A  T"
    if day==6:
        txt="S  U  N"
    return txt

def get_total_days():
    today=get_today()
    if today.month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif today.month == 2:
        return 29 if (today.year % 4 == 0 and today.year % 100 != 0) or (today.year % 400 == 0) else 28
    else:
        return 30

def get_days_remaining_in_month():
    today = get_today()
    total_days = get_total_days()
    return total_days - today.day