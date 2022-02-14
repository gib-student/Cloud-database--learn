from datetime import date

todays_date = date.today()
days = ["Mon","Tue","Wed","Thu","Fri","Sat", "Sun"]

weekday = todays_date.weekday()

print(weekday)