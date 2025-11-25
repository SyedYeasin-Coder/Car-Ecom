function updateFilters() {
    const model = document.getElementById("modelSelect").value;
    const city = document.getElementById("citySelect").value;
    const year = document.getElementById("yearSelect").value;
    const body = document.getElementById("bodyStyleSelect").value;
    const transmissionEl = document.getElementById("transmissionSelect");
    const transmission = transmissionEl ? transmissionEl.value : '';

    // Build URL dynamically to handle missing transmission
    let url = `${filterOptionsUrl}?model=${model}&city=${city}&year=${year}&body_style=${body}`;
    if(transmissionEl) {
        url += `&transmission=${transmission}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateDropdown("modelSelect", "Select Model", data.models);
            updateDropdown("citySelect", "Select Location", data.cities);
            updateDropdown("yearSelect", "Select Year", data.years);
            updateDropdown("bodyStyleSelect", "Select Type Of Car", data.body_styles);
            if(transmissionEl) {
                updateDropdown("transmissionSelect", "Transmission", data.transmissions);
            }
        });
}

function updateDropdown(selectId, placeholder, options) {
    const select = document.getElementById(selectId);
    const currentValue = select.value;

    select.innerHTML = `<option value="">${placeholder}</option>`;
    options.forEach(option => {
        select.innerHTML += `<option value="${option}">${option}</option>`;
    });

    // Re-select the previously selected value if it still exists
    if (options.includes(currentValue)) {
        select.value = currentValue;
    }
}

// Attach change events
["modelSelect", "citySelect", "yearSelect", "bodyStyleSelect", "transmissionSelect"].forEach(id => {
    const el = document.getElementById(id);
    if(el) el.addEventListener("change", updateFilters);
});
