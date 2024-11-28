import time
from datetime import datetime

def current_time_in_ms():
    return int(time.time() * 1000)

def current_date():
    return datetime.now().strftime('%Y-%m-%d')

def current_day():
    return datetime.now().strftime('%A')
