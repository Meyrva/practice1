#1  subtract five days from current date
import datetime
x = datetime.datetime.now()

a = x.day
# print(a)
print(a-5)

#2  yesterday, today, tomorrow
print("yesterday:",a-1)
print("today:",a)
print("tomorrow:", a+1)


#3  microseconds 
print(x.strftime("%f"))


#4  two date difference in seconds
one = datetime.datetime(2025, 6, 1, 21, 7, 46)
two = datetime.datetime(2023, 10, 21, 18, 30, 3)
print(int(one.strftime("%S")) - int(two.strftime("%S")))



