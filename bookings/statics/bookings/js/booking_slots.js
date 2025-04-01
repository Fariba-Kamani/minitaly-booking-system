
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
        if (data.slots && data.slots.length > 0) {
            let anyAvailable = false;
          
            data.slots.forEach(slot => {
              const option = document.createElement('option');
              option.value = slot.time;
              option.textContent = slot.time;
              if (!slot.available) {
                option.disabled = true;
                option.textContent += " (Full)";
              } else {
                anyAvailable = true;
              }
              timeField.appendChild(option);
            });
          
            if (!anyAvailable) {
              const noOption = document.createElement('option');
              noOption.textContent = "No available time slots";
              noOption.disabled = true;
              noOption.selected = true;
              timeField.innerHTML = '';
              timeField.appendChild(noOption);
            }
          
          } else {
            const noOption = document.createElement('option');
            noOption.textContent = "No available time slots";
            noOption.disabled = true;
            noOption.selected = true;
            timeField.appendChild(noOption);
          }
          
      });
  }

  dateField.addEventListener('change', loadAvailableSlots);
  guestField.addEventListener('change', loadAvailableSlots);
