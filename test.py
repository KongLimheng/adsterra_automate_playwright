from datetime import datetime, timedelta


now = datetime.now()
next_date = now + timedelta(minutes=int(600 / 60))

print(next_date.strftime("%Y-%m-%d %I:%M %p"))
