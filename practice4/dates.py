# Practice 04 - Dates and Time

from datetime import datetime, date, time, timedelta, timezone

now = datetime.now()
today = date.today()

print("Current date and time:", now)
print("Today's date:", today)

# Creating date objects
birthday = date(2008, 5, 15)
print("\nCreated date:", birthday)

# Creating a datetime object
event = datetime(2026, 10, 1, 14, 30)
print("Event date and time:", event)

# Date formatting
print("\nFormatted date:")
print(now.strftime("%Y-%m-%d"))
print(now.strftime("%d/%m/%Y"))
print(now.strftime("%B %d, %Y"))
print(now.strftime("%A, %B %d, %Y %H:%M"))

# String to datetime
date_string = "2026-09-28 18:30"
parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
print("\nParsed date:", parsed_date)

# Calculating time differences
start = datetime(2026, 9, 28, 10, 0)
end = datetime(2026, 9, 28, 15, 30)
difference = end - start

print("\nTime difference:", difference)
print("Difference in hours:", difference.total_seconds() / 3600)

# Adding and subtracting time
print("\nTomorrow:", today + timedelta(days=1))
print("Next week:", today + timedelta(weeks=1))
print("Three days ago:", today - timedelta(days=3))

# Time object
meeting_time = time(14, 30)
print("\nMeeting time:", meeting_time)

# Timezones
utc_time = datetime.now(timezone.utc)
almaty_offset = timezone(timedelta(hours=5))
almaty_time = datetime.now(almaty_offset)

print("\nUTC time:", utc_time)
print("Almaty time (UTC+5):", almaty_time)
