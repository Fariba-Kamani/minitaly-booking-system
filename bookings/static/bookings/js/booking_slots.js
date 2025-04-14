/* jshint esversion: 6 */
/* global initialTime, initialDate, initialGuests */
// Get form input fields for date, number of guests, and time
const dateField = document.getElementById('id_date');
const guestField = document.getElementById('id_num_guests');
const timeField = document.getElementById('id_time');

// --- Utility ---

/**
 * Normalize time strings to "HH:MM:SS" format.
 * Ensures compatibility with Django backend (which stores time as full format).
 * Example: "19:00" → "19:00:00"
 */
function normalizeTimeFormat(timeStr) {
  if (timeStr && timeStr.length === 5) {
    return timeStr + ':00';
  }
  return timeStr;
}

// Normalize the initially loaded time from the template (if any)
const normalizedInitialTime = normalizeTimeFormat(initialTime);

// --- Main logic ---

/**
 * Fetch available time slots from the API and populate the time <select> field.
 * Disables fully booked options and pre-selects previously selected time if still valid.
 */
function loadAvailableSlots() {
  const date = dateField.value;
  const guests = guestField.value;

  if (!date || !guests) return; // Don’t run until both fields are filled

  fetch(`/bookings/api/available-slots/?date=${date}&guests=${guests}`)
    .then(res => res.json())
    .then(data => {
      timeField.innerHTML = ''; // Clear previous options
      let anyAvailable = false;
      let timeMatched = false;

      // Loop through available slots and create <option> elements
      data.slots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot.time;
        option.textContent = slot.time;

        // Disable unavailable slots unless it's the originally selected one
        if (!slot.available && slot.time !== normalizedInitialTime) {
          option.disabled = true;
          option.textContent += " (Full)";
        } else {
          anyAvailable = true;
        }

        // Restore previous selection if possible
        if (slot.time === normalizedInitialTime) {
          option.selected = true;
          timeMatched = true;
        }

        timeField.appendChild(option);
      });

      // If no slots available and no original time, show fallback message
      if (!anyAvailable && !normalizedInitialTime) {
        const noOption = document.createElement('option');
        noOption.textContent = "No available time slots";
        noOption.disabled = true;
        noOption.selected = true;
        timeField.appendChild(noOption);
      }

      // If the original time isn't in the list (but still valid), add it
      if (!timeMatched && normalizedInitialTime) {
        const originalOption = document.createElement('option');
        originalOption.value = normalizedInitialTime;
        originalOption.textContent = normalizedInitialTime;
        originalOption.selected = true;
        timeField.appendChild(originalOption);
      }
    });
}

// --- Event listeners ---

// Load available time slots whenever date or guest count changes
dateField.addEventListener('change', loadAvailableSlots);
guestField.addEventListener('change', loadAvailableSlots);

// On page load: set values and trigger initial slot loading
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
