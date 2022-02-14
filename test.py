from ctypes import create_unicode_buffer
from datetime import date
todays_date = date.today()
current_year = todays_date.year
current_month = todays_date.month
months = [
    "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
    ]
_ledger = {
    '2021': {"Oct": [200, 100]}
}

def record_deposit(new_funds, ledger):
    # Check if there is a year in the ledger for the current year
    # If not, then add the current year and month
    if ((not str(current_year) in ledger) or 
       (not months[current_month - 1] in ledger[str(current_year)])):
        ledger[str(current_year)] = {months[current_month - 1]: []}
    # Record the deposit
    ledger[str(current_year)][months[current_month - 1]].append(new_funds)

    return ledger
    # Record the deposit
print(record_deposit(500, _ledger))