from datetime import datetime, timedelta
from collections import defaultdict
from .constants import OPERATING_HOURS, TABLE_INVENTORY, MAX_GUESTS_PER_BOOKING
from .models import Booking

def generate_time_slots(date: datetime.date):
    slots = []
    current = datetime.combine(date, OPERATING_HOURS['start'])
    end_time = datetime.combine(date, OPERATING_HOURS['end'])

    while current <= end_time:
        slots.append(current.time())
        current += OPERATING_HOURS['interval']
    
    return slots

def get_available_time_slots(date, num_guests):
    all_slots = generate_time_slots(date)
    bookings = Booking.objects.filter(date=date)

     # Build a tracker for booked tables
    booked = defaultdict(lambda: defaultdict(int))  # {time: {size: count}}

    for b in bookings:
        booked[b.time][b.num_guests] += 1

    available_slots = []

    for slot in all_slots:
        suitable_sizes = [size for size in TABLE_INVENTORY if size >= num_guests and size <= MAX_GUESTS_PER_BOOKING]

        available = False
        for size in suitable_sizes:
            if booked[slot][size] < TABLE_INVENTORY[size]:
                available = True
                break

        available_slots.append({
            "time": slot,
            "available": available
        })

    return available_slots