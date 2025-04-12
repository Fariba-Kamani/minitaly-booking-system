"""
constants.py

Defines static configuration values for the restaurant booking system.

This includes:
- Operating hours and intervals
- Table inventory by size
- Maximum allowed guest count per booking
"""

from datetime import time, timedelta

# Restaurant operating hours and time slot settings
OPERATING_HOURS = {
    'start': time(17, 0),   # Restaurant opens at 17:00 (5 PM)
    'end': time(22, 0),     # Last booking slot is 22:00 (10 PM)
    'interval': timedelta(hours=1),  # Time slots are spaced 1 hour apart
    'sitting_duration': timedelta(hours=2),  # Each party can stay up to 2 hours
}

# Table availability by size (capacity: number of tables)
TABLE_INVENTORY = {
    2: 4,   # 4 tables that seat 2 guests
    4: 5,   # 5 tables that seat 4 guests
    6: 4,   # 4 tables that seat 6 guests
    8: 1,   # 1 table that seats 8 guests
    10: 1,  # 1 table that seats 10 guests
}

# Upper limit for how many guests can be booked in a single reservation
# For larger groups, customers must call the restaurant directly
MAX_GUESTS_PER_BOOKING = 10
