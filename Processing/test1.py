import datetime
current_timestamp = datetime.datetime.now()
t = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
print(t)