# bookings/constants.py
from datetime import time, timedelta, datetime

OPERATING_HOURS = {
    'start': time(17, 0),   # 17:00
    'end': time(22, 0),     # 22:00
    'interval': timedelta(hours=1),  # 1-hour interval
    'sitting_duration': timedelta(hours=2),  # Guests can stay for 2 hours
}