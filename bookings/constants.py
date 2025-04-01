# bookings/constants.py
from datetime import time, timedelta, datetime

OPERATING_HOURS = {
    'start': time(17, 0),   # 17:00
    'end': time(22, 0),     # 22:00
    'interval': timedelta(hours=1),  # 1-hour interval
    'sitting_duration': timedelta(hours=2),  # Guests can stay for 2 hours
}

TABLE_INVENTORY = {
    2: 4,   # 4 tables for 2 guests
    4: 5,   # 5 tables for 4 guests
    6: 4,   # 4 tables for 6 guests
    8: 1,   # 1 table for 8 guests
    10: 1,  # 1 table for 10 guests
}

MAX_GUESTS_PER_BOOKING = 10