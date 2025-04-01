# bookings/utils.py
from datetime import datetime, timedelta
from .constants import OPERATING_HOURS

def generate_time_slots(date: datetime.date):
    slots = []
    current = datetime.combine(date, OPERATING_HOURS['start'])
    end_time = datetime.combine(date, OPERATING_HOURS['end'])

    while current <= end_time:
        slots.append(current.time())
        current += OPERATING_HOURS['interval']
    
    return slots