import time

mytime = time.localtime()
if mytime.tm_hour < 6 or mytime.tm_hour > 18:
    a = 0
else:
    a = 1


def checklightcondition():
    return a



