const dateField = document.getElementById('id_date');
const guestField = document.getElementById('id_num_guests');
const timeField = document.getElementById('id_time');

function loadAvailableSlots() {
  const date = dateField.value;
  const guests = guestField.value;

  if (!date || !guests) return;

  fetch(`/bookings/api/available-slots/?date=${date}&guests=${guests}`)
    .then(res => res.json())
    .then(data => {
      timeField.innerHTML = '';
      let anyAvailable = false;

      data.slots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot.time;
        option.textContent = slot.time;

        console.log("slot.time:", slot.time, "initialTime:", initialTime);

        if (!slot.available && slot.time !== initialTime) {
          option.disabled = true;
          option.textContent += " (Full)";
        } else {
          anyAvailable = true;
        }

        if (slot.time === initialTime) {
            option.selected = true;
            timeMatched = true;
          }

        timeField.appendChild(option);
      });

      if (!anyAvailable && !initialTime) {
        const noOption = document.createElement('option');
        noOption.textContent = "No available time slots";
        noOption.disabled = true;
        noOption.selected = true;
        timeField.appendChild(noOption);
      }
    });
}

// Trigger updates when fields change
dateField.addEventListener('change', loadAvailableSlots);
guestField.addEventListener('change', loadAvailableSlots);

// 👇 This block is for EDIT VIEW pre-filling
document.addEventListener('DOMContentLoaded', () => {
  if (initialDate && initialGuests) {
    dateField.value = initialDate;
    guestField.value = initialGuests;

    fetch(`/bookings/api/available-slots/?date=${initialDate}&guests=${initialGuests}`)
      .then(res => res.json())
      .then(data => {
        timeField.innerHTML = '';
        let timeMatched = false;

        data.slots.forEach(slot => {
          const option = document.createElement('option');
          option.value = slot.time;
          option.textContent = slot.time;

          if (!slot.available && slot.time !== initialTime) {
            option.disabled = true;
            option.textContent += " (Full)";
          }

          if (slot.time === initialTime) {
            option.selected = true;
            timeMatched = true;
          }

          timeField.appendChild(option);
        });

        // If the current booking time is no longer available, still show it
        if (!timeMatched && initialTime) {
          const originalOption = document.createElement('option');
          originalOption.value = initialTime;
          originalOption.textContent = `${initialTime} (Your original time)`;
          originalOption.selected = true;
          timeField.appendChild(originalOption);
        }
      });
  }
});
