myString = "Hello there !bob@"
mySubString = myString[myString.find("!") + 1:myString.find("@")]
print mySubString

s = "log-20120616.gz"
LOG_MONTH = s[8:10]
print LOG_MONTH


from datetime import datetime, timedelta

now = datetime.now()
now.date()
# datetime.date(2011, 3, 29)
now.replace(hour=0, minute=0, second=0, microsecond=0)
# datetime.datetime(2011, 3, 29, 0, 0)

d2 = now.date()
print "Estamos a " + str(d2)
initial_date = "20130122"
i_year = int(initial_date[:4])
i_month = int(initial_date[4:6])
i_day = int(initial_date[6:])

d1 = now.replace(year=i_year, month=i_month, day=i_day, hour=0, minute=0, second=0, microsecond=0).date()

while d1 <= d2:
	print d1
	d1 += timedelta(1)
