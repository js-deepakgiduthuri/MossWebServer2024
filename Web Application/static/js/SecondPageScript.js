function openTab(evt, optionName) {
  var i, tabcontent, tablinks;

  // Hide all tab content
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove 'active' class from all tab links
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the selected tab content and set 'active' class to the button that opened the tab
  document.getElementById(optionName).style.display = "flex";
  evt.currentTarget.className += " active";

  if (optionName === "State") {
    fetch('/static/data.json')
      .then(response => response.json())
      .then(data => displayStateParams(data))
      .catch(error => console.log(error));
  }

  if (optionName === "APNs") {
    fetch('/get_apn')
      .then(response => response.json())
      .then(data => populateApnDropdown(data))
      .catch(error => console.log(error));
  }
}

// Additional event listeners and helper functions
document.addEventListener("DOMContentLoaded", function() {
  var ipAddressSelect = document.getElementById("ip-address-type");
  var ipAddressInput = document.getElementById("ip-address");
  var subnetMaskInput = document.getElementById("subnet-mask");
  var gatewayInput = document.getElementById("gateway");
  var dnsServerInput = document.getElementById("dns-server");
  var dnsSecondaryInput = document.getElementById("dns-secondary");

  ipAddressSelect.addEventListener("change", function() {
    var selectedOption = ipAddressSelect.value;
    if (selectedOption === "dynamic") {
      ipAddressInput.disabled = true;
      subnetMaskInput.disabled = true;
      gatewayInput.disabled = true;
      dnsServerInput.disabled = true;
      dnsSecondaryInput.disabled = true;
    } else {
      ipAddressInput.disabled = false;
      subnetMaskInput.disabled = false;
      gatewayInput.disabled = false;
      dnsServerInput.disabled = false;
      dnsSecondaryInput.disabled = false;
    }
  });

  var addApnButton = document.getElementById("add-apn");
  if (addApnButton) {
    addApnButton.addEventListener("click", function() {
      window.location.href = "/add_apn";
    });
  }

  var removeApnButton = document.getElementById("remove-apn");
  if (removeApnButton) {
    removeApnButton.addEventListener("click", function() {
      window.location.href = "/remove_apn";
    });
  }
});

function displayStateParams(data) {
  var stateParamsContainer = document.getElementById("stateParamsContainer");
  stateParamsContainer.innerHTML = "";

  var paramsTitle = document.createElement("h2");
  paramsTitle.textContent = "State Parameters";
  stateParamsContainer.appendChild(paramsTitle);

  for (var key in data) {
    var label = document.createElement("label");
    label.classList.add("param-label");
    label.textContent = key + ":";
    stateParamsContainer.appendChild(label);

    var value = document.createElement("span");
    value.classList.add("param-value");
    var paramValue = data[key];

    if (typeof paramValue === "object") {
      value.textContent = JSON.stringify(paramValue);
    } else {
      value.textContent = " " + paramValue;
    }

    stateParamsContainer.appendChild(value);
    var lineBreak = document.createElement("br");
    stateParamsContainer.appendChild(lineBreak);
  }
}

function populateApnDropdown(apnData) {
  var apnDropdown = document.getElementById("apn-dropdown");
  apnDropdown.innerHTML = "";

  for (var key in apnData) {
    var option = document.createElement("option");
    option.value = key;
    option.textContent = key + ": " + apnData[key];
    apnDropdown.appendChild(option);
  }
}

function refreshLAN() {
  const lanContainer = document.getElementById('lan-content');
  lanContainer.innerHTML = ''; // Clear existing content

  fetch('/read_ethernet')
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      return response.json();
    })
    .then(data => {
      if (data.error) throw new Error(data.error);

      // Loop through each key-value pair and format with bold keys
      for (const [key, value] of Object.entries(data)) {
        const item = document.createElement('div');
        item.classList.add('dictionary-item');

        // Add the key in bold using innerHTML
        item.innerHTML = `<strong>${key}:</strong> ${value}`;

        lanContainer.appendChild(item);
      }
    })
    .catch(error => {
      console.error('Error fetching Ethernet data:', error);
      lanContainer.innerHTML = '<div class="dictionary-item">Error loading Ethernet data.</div>';
    });
}

document.addEventListener('DOMContentLoaded', refreshLAN);
