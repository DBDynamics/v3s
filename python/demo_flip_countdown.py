from libflip import Flip
import time
import os

f = Flip()
f.initDevice()
f.homeAll()
time.sleep(60*3)
os.system("/usr/bin/python3 /root/timesync.py")
# 10 9 8 7 / 6 5/ 4 3 /210
#2122 01 01 00s
# for i in range(0, 30):
#     time.sleep(1)
#     for axis in range(4, 8):
#         f.flipNPage(axis, 1)



import time
from datetime import datetime

# Set the target date
target_date = datetime(2122, 1, 1, 0, 0, 0)


counter = 0
while True:
    # Get the current date and time
    now = datetime.now()
    # Calculate the difference
    countdown = target_date - now

    # Extract the remaining time components
    years = countdown.days // 365
    months = (countdown.days % 365) // 30
    days = (countdown.days % 365) % 30
    hours, remainder = divmod(countdown.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Print the countdown
    print(f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds remaining.")
    
    td = countdown.days*24*60*60
    ts = countdown.total_seconds()
    print(f"days:{countdown.days},secs:{countdown.seconds}")
    num_0 = ts%10
    num_1 = (int)(ts/10)%10
    num_2 = (int)(ts/100)%10
    num_3 = (int)(ts/1000)%10
    num_4 = (int)(ts/10000)%10
    num_5 = (int)(ts/100000)%10
    num_6 = (int)(ts/1000000)%10
    num_7 = (int)(ts/10000000)%10
    num_8 = (int)(ts/100000000)%10
    num_9 = (int)(ts/1000000000)%10
    # num_10 = (int)(ts/1000000000)%10
    print(num_1, num_0)
    f.displayNum(0, num_0)
    f.displayNum(1, num_0)
    f.displayNum(2, num_1)
    f.displayNum(3, num_2)
    f.displayNum(4, num_3)
    f.displayNum(5, num_4)
    f.displayNum(6, num_5)
    f.displayNum(7, num_6)
    f.displayNum(8, num_7)
    f.displayNum(9, num_8)
    f.displayNum(10, num_9)
    # f.displayNum(11, num_10)

    counter += 1
    if counter > 60*60*12:
        counter = 0
        os.system("/usr/bin/python3 /root/timesync.py")
    # Wait for one second
    time.sleep(1)


f.stop()