const dateField = document.getElementById('id_date');
const guestField = document.getElementById('id_num_guests');
const timeField = document.getElementById('id_time');

// Normalize to HH:MM:SS format if needed
function normalizeTimeFormat(timeStr) {
  if (timeStr && timeStr.length === 5) {
    return timeStr + ':00'; // Convert "19:00" → "19:00:00"
  }
  return timeStr;
}

const normalizedInitialTime = normalizeTimeFormat(initialTime);

function loadAvailableSlots() {
  const date = dateField.value;
  const guests = guestField.value;

  if (!date || !guests) return;

  fetch(`/bookings/api/available-slots/?date=${date}&guests=${guests}`)
    .then(res => res.json())
    .then(data => {
      timeField.innerHTML = '';
      let anyAvailable = false;
      let timeMatched = false;

      data.slots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot.time;
        option.textContent = slot.time;

        if (!slot.available && slot.time !== normalizedInitialTime) {
          option.disabled = true;
          option.textContent += " (Full)";
        } else {
          anyAvailable = true;
        }

        if (slot.time === normalizedInitialTime) {
          option.selected = true;
          timeMatched = true;
        }

        timeField.appendChild(option);
      });

      if (!anyAvailable && !normalizedInitialTime) {
        const noOption = document.createElement('option');
        noOption.textContent = "No available time slots";
        noOption.disabled = true;
        noOption.selected = true;
        timeField.appendChild(noOption);
      }

      if (!timeMatched && normalizedInitialTime) {
        const originalOption = document.createElement('option');
        originalOption.value = normalizedInitialTime;
        originalOption.textContent = normalizedInitialTime;
        originalOption.selected = true;
        timeField.appendChild(originalOption);
      }
    });
}

// Trigger updates when fields change
dateField.addEventListener('change', loadAvailableSlots);
guestField.addEventListener('change', loadAvailableSlots);

// 👇 On page load, ensure fields are populated and fetch correct slots
document.addEventListener('DOMContentLoaded', () => {
  if (initialDate) {
    dateField.value = initialDate;
  }

  if (initialGuests) {
    guestField.value = initialGuests;
  }

  if (initialDate && initialGuests) {
    loadAvailableSlots();
  }
});
