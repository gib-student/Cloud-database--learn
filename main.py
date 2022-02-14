"""
CSE310 Cloud Database Workshop - Solution

This program will allow you to manage funds in a firestore Cloud
database.

"""

from calendar import month
from string import printable
from tokenize import triple_quoted
from turtle import update
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date
import os

# Constants
todays_date = date.today()
current_year = todays_date.year
current_month = todays_date.month
months = [
    "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"
    ]
funds_key = "funds"
ledger_key = "ledger"

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "cse310-myproject-firebase-adminsdk-xir8r-37d60d38a1.json"

    # Use the application default credentials.  The projectID is obtianed
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'cse310-myproject',
    })

    # Get reference to database
    db = firestore.client()
    return db

def initialize_docs(db):
    '''
    Initialize funds and ledger documents if they are not already
    '''
    result  = db.collection("financial").document(funds_key).get()
    result2 = db.collection("financial").document(ledger_key).get()

    # Check if funds doc exist
    if not result.exists:
        funds   = {"funds": 0}
        update_funds_db(db, funds)
    # Check if ledger doc exists
    if not result2.exists:
        ledger = new_ledger()
        update_ledger_db(db, ledger)

def add_funds(db, funds, ledger):
    '''
    Add funds
    '''
    # Get new funds
    new_funds = int(input("New funds to add in dollars: "))

    # Add new funds
    current_funds = funds[funds_key]
    sum_funds = current_funds + new_funds
    funds[funds_key] = sum_funds
    update_funds_db(db, funds)

    # Record the deposit
    ledger = record_deposit(new_funds, ledger)
    update_ledger_db(db, ledger)

    # Display new balance
    print_balance(funds)

def record_deposit(new_funds, ledger):
    # Validate ledger
    ledger = check_year_month_ledger(ledger)
    # Record the deposit
    ledger[str(current_year)][months[current_month - 1]].append(new_funds)
    
    return ledger

def subtract_expense(db, funds, ledger):
    '''
    Record expense
    '''
    # Get expense info
    expense = int(input("Value of the expense: "))

    # Subtract funds
    funds_value = funds[funds_key]
    new_funds_value = funds_value - expense
    funds[funds_key] = new_funds_value
    update_funds_db(db, funds)

    # Record the expense
    ledger = record_expense(db, ledger, expense)
    update_ledger_db(db, ledger)

    # Display new balance
    print_balance(funds)

def record_expense(db, ledger, expense):
    # Validate ledger
    ledger = check_year_month_ledger(ledger)
    # Record the expense
    expense_negative = -expense
    ledger[str(current_year)][months[current_month - 1]].append(expense_negative)

    return ledger

def print_balance(funds):
    balance = funds[funds_key]
    print("Balance: $" + str(balance))

def view_trans_history(ledger):
    # Ask for year and then a month
    year = str(input("Year you would you like to view for: "))
    month = str(input("Month you would like to view for: "))

    # Display the history
    # Display year
    print(year)
    counter = 1
    for transaction in ledger[year][month]:
        print(str(counter) + ". ", end="")
        if transaction > 0:
            print("+$" + str(transaction))
        else:
            print("$" + str(transaction))
        counter += 1


def new_ledger():
    ledger = {
        str(current_year): {
            months[current_month - 1]: []
        }
    }
    return ledger

def get_funds_dict(db):
    result = db.collection("financial").document(funds_key).get()
    return result.to_dict()

def get_ledger_dict(db):
    result2 = db.collection("financial").document(ledger_key).get()
    return result2.to_dict()

def update_funds_db(db, funds):
    db.collection("financial").document(funds_key).set(funds)

def update_ledger_db(db, ledger):
    db.collection("financial").document(ledger_key).set(ledger)

def check_year_month_ledger(ledger):
    # Check if there is a year in the ledger for the current year
    # If not, then add the current year and month
    if ((not str(current_year) in ledger) or
       (not months[current_month - 1] in ledger[str(current_year)])):
        ledger[str(current_year)] = {months[current_month - 1]: []}
    return ledger

'''*********************MAIN*******************'''
def main():
    db = initialize_firestore()
    # If a funds category has not yet been made, then make one
    initialize_docs(db)
    funds = get_funds_dict(db)
    ledger = get_ledger_dict(db)
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add Funds")
        print("2) Record Expense")
        print("3) View Balance")
        print("4) View Transaction History")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_funds(db, funds, ledger)
        elif choice == "2":
            subtract_expense(db, funds, ledger)
        elif choice == "3":
            print_balance(funds)
        elif choice == "4":
            view_trans_history(ledger)

if __name__ == "__main__":
    main()
