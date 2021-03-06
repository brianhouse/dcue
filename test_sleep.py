#!/usr/bin/env python3

from datetime import datetime
import time

def check_sleep(amount):
    start = datetime.now()
    time.sleep(amount)
    end = datetime.now()
    delta = end - start
    return delta.seconds + (delta.microseconds / 1000000.)

error = sum(abs(check_sleep(0.010) - 0.010) for i in range(100)) * 10
print("Average error is %0.2fms" % error)