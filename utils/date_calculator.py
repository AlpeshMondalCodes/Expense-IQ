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