// All-Use
function toggleDropdown(dropdown) {
    var content = dropdown.nextElementSibling;
    content.style.display = content.style.display === 'block' ? 'none' : 'block';
    dropdown.classList.toggle('active');
}


function hideAllDropdowns() {
    var dropdowns = document.querySelectorAll(".dropdown");
    for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.style.display === 'block') {
            openDropdown.style.display = 'none';
            openDropdown.previousElementSibling.classList.remove('active');
        }
    }
}

function handleDropdownButtonClick(event) {
    event.stopPropagation();
    hideAllDropdowns();
    toggleDropdown(this);
}

var dropdownButtons = document.querySelectorAll(".dropdown-btn");
dropdownButtons.forEach(function (button) {
    button.addEventListener("click", handleDropdownButtonClick);
});


// Sample of using toggleDropdown for specific dropdown
var specificDropdownButton = document.getElementById("specificDropdownBtn");
specificDropdownButton.addEventListener("click", function () {
    toggleDropdown(this);
});

////////////////////////////////////////////////// add_polling ////////////////////////////////////////////////////////////

function saveToOracle() {
    var data = {};

    // Include EVC_TYPE in data
    data.evc_type = document.getElementById("evc_type").value;

    // Loop through address pairs 1 through 15
    for (var i = 1; i <= 15; i++) {
        var startKey = 'start' + i;
        var endKey = 'end' + i;
        var enableKey = 'enable' + i;

        data[startKey] = document.getElementById(startKey).value;
        data[endKey] = document.getElementById(endKey).value;
        data[enableKey] = document.getElementById(enableKey).checked ? 1 : 0;

        // Ensure all start and end values are provided
        if (!data[startKey] || !data[endKey]) {
            document.getElementById("statusMessage").innerHTML = "Please enter both start and end addresses for all pairs.";
            return;
        }
    }

    // Assuming 'data' contains the necessary start and end values
    data.enable_config = [];
    data.enable_billing = [];

    for (let i = 1; i <= 15; i++) {
        if (data[`enable${i}`] !== undefined) {
            if (i <= 5) {
                data.enable_config.push(parseInt(data[`enable${i}`]));
            } else {
                data.enable_billing.push(parseInt(data[`enable${i}`]));
            }
        }
    }

    fetch('/save_to_oracle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            document.getElementById("statusMessage").innerHTML = data.message;
        })
        .catch((error) => {
            console.error('Error:', error);
            document.getElementById("statusMessage").innerHTML = "An error occurred while saving data.";
        });
}

////////////////////////////////////////////////// add_polling ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// add_user ////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.querySelectorAll('.flash-messages li');

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s';

            setTimeout(function () {
                message.style.display = 'none';
            }, 500);
        }, 3000); // Adjust the timeout value (in milliseconds) as needed
    });
});



////////////////////////////////////////////////// add_user ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// billing_data ////////////////////////////////////////////////////////////

function checkFormSubmission(queryType) {
    // Check if region, site, and date are selected
    var region = document.getElementById("region_dropdown").value;
    var site = document.getElementById("tag_dropdown").value;
    var date = document.getElementById("date_picker").value;

    if (queryType === "daily_data" && (region === "" || site === "" || date === "")) {
        alert("Please select Region, Site, and Date before submitting.");
        return false;
    } else if (queryType === "config_data" && (region === "" || site === "" || date === "")) {
        alert("Please select Region, Site, and Date before submitting.");
        return false;
    }

    return true;
}

function clearFilters() {
    // Clear selected values
    document.getElementById("region_dropdown").value = "";
    document.getElementById("tag_dropdown").value = "";
    document.getElementById("date_picker").value = "";
}
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'block';
}


var None = document.getElementById("None");

function toggleDiv() {
    if (None.style.display === "none") {
        None.style.display = "block";
    } else {
        None.style.display = "none";
    }
}

toggleDiv();

// Event listener for form submission with 'daily_data' event
var formDailyData = document.querySelector('form[action="/billing_data"]'); // Adjust this selector based on your actual form
formDailyData.addEventListener('config_data', function (event) {
    event.preventDefault(); // Prevent the form from submitting immediately

    showLoadingOverlay();

    // Simulate delay with setTimeout (you can replace this with your actual loading logic)
    setTimeout(function () {
        // Update the displayed values after the loading is complete
        document.getElementById('selected_region').innerText = selectedRegion;
        document.getElementById('selected_tag').innerText = selectedTag;
        document.getElementById('selected_date').innerText = selectedDate;

        // Optionally, update the meter ID
        var selectedMeterIdSpan = document.getElementById('selected_meter_id');
        if (selectedMeterIdSpan) {
            selectedMeterIdSpan.innerText = "{{ selected_meter_id }}"; // Replace with your actual meter ID variable
        }

        // Reset selected values
        selectedRegion = null;
        selectedTag = null;
        selectedDate = null;

        // Submit the form programmatically
        formDailyData.submit();
    }, 2000); // Adjust the delay time as needed (in milliseconds)
});

// Event listener for form submission with 'config_data' event
var formConfigData = document.querySelector('form[action="/billing_data"]'); // Adjust this selector based on your actual form
formConfigData.addEventListener('daily_data', function (event) {
    event.preventDefault(); // Prevent the form from submitting immediately

    showLoadingOverlay();

    // Simulate delay with setTimeout (you can replace this with your actual loading logic)
    setTimeout(function () {
        // Update the displayed values after the loading is complete
        document.getElementById('selected_region').innerText = selectedRegion;
        document.getElementById('selected_tag').innerText = selectedTag;
        document.getElementById('selected_date').innerText = selectedDate;

        // Optionally, update the meter ID
        var selectedMeterIdSpan = document.getElementById('selected_meter_id');
        if (selectedMeterIdSpan) {
            selectedMeterIdSpan.innerText = "{{ selected_meter_id }}"; // Replace with your actual meter ID variable
        }

        // Reset selected values
        selectedRegion = null;
        selectedTag = null;
        selectedDate = null;

        // Submit the form programmatically
        formConfigData.submit();
    }, 2000); // Adjust the delay time as needed (in milliseconds)
});

function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}


// Wait for the document to be ready
$(document).ready(function () {
    $('#date_picker').datepicker({
        format: 'mm/yyyy',
        startView: 'months',
        minViewMode: 'months',
        autoclose: true
    });

    // Event listener for region dropdown change
    $('#region_dropdown').change(function () {
        var selectedRegion = $(this).val();

        $.ajax({
            type: 'GET',
            url: '/get_tags',
            data: { 'selected_region': selectedRegion },
            success: function (response) {
                // Clear existing options in the tag dropdown
                $('#tag_dropdown').empty();
                // Add the 'All' option
                $('#tag_dropdown').append('<option value="" selected>All</option>');
                // Add new tag options based on the response
                for (var i = 0; i < response.tag_options.length; i++) {
                    var tag = response.tag_options[i];
                    $('#tag_dropdown').append('<option value="' + tag + '">' + tag + '</option>');
                }
                hideLoadingOverlay(); // Hide loading overlay after successful AJAX request
            },
            error: function (error) {
                console.log('Error fetching tag options:', error);
                hideLoadingOverlay(); // Hide loading overlay after AJAX request error
            }
        });
    });
});

////////////////////////////////////////////////// billing_data ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// Daily_summary ////////////////////////////////////////////////////////////

$(document).ready(function () {
    $('#date_picker').datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true
    });

    hideCircle();
});

$(document).ready(function () {
    $('#region_dropdown').change(function () {
        var selectedRegion = $(this).val();
        $.ajax({
            type: 'GET',
            url: '/get_tags',
            data: { 'selected_region': selectedRegion },
            success: function (response) {
                response.tag_options.sort(function (a, b) {
                    return a.localeCompare(b);
                });
                var tagDropdown = $('#tag_dropdown');
                tagDropdown.empty();
                $.each(response.tag_options, function (index, tagOption) {
                    tagDropdown.append('<option value="' + tagOption + '">' + tagOption + '</option>');
                });

                hideCircle();
            },
            error: function (error) {
                console.log('Error fetching tag options:', error);
            }
        });
    });
});

function hideCircle() {
    $('td:after').hide();
}

////////////////////////////////////////////////// Daily_summary ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// edit_user ////////////////////////////////////////////////////////////

$(document).ready(function() {
    // Load data from server
    $.getJSON('/get_data', function(data) {
        // Sort data alphabetically by description
        data.sort(function(a, b) {
            return a.description.localeCompare(b.description);
        });

        // Populate dropdown with sorted data
        var dropdown = $('#myDropdown');
        $.each(data, function(index, value) {
            var optionText = value.description;
            var optionValue = JSON.stringify(value);
            dropdown.append($('<option>').text(optionText).attr('value', optionValue));
        });

        // Set initial details
        var initialData = data[0];
        displayDetails(initialData);
    });

    // Function to display details when an item is selected
    $('#myDropdown').change(function() {
        var selectedData = JSON.parse($(this).val());
        displayDetails(selectedData);
    });

    // Function to display details
    function displayDetails(selectedData) {
        $('#details #description').val(selectedData.description);
        $('#details #user_name').val(selectedData.user_name);
        $('#details #password').val(""); // Clear password field for security
        $('#details #user_level').val(selectedData.user_level);
    }
});

////////////////////////////////////////////////// edit_user ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// home ////////////////////////////////////////////////////////////

const WebManager = {
    updateTime: function () {
        const today = new Date();
        const date = today.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        const time = today.toLocaleTimeString();
        document.getElementById('datetime').innerHTML = `${date} - ${time}`;
    },

    setupDropdowns: function () {
        var dropdown = document.getElementsByClassName("dropdown-btn");
        for (var i = 0; i < dropdown.length; i++) {
            dropdown[i].addEventListener("click", function () {
                this.classList.toggle("active");
                WebManager.toggleDropdown(this);
            });
        }
    },

    startUpdatingTime: function () {
        WebManager.updateTime();
        setInterval(WebManager.updateTime, 1000);
    },

    init: function () {
        WebManager.startUpdatingTime();
        WebManager.setupDropdowns();
    }
};

WebManager.init();

////////////////////////////////////////////////// home ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// login ////////////////////////////////////////////////////////////

var myInput = document.getElementById("psw");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

var showPassword = document.getElementById("togglePassword");
showPassword.addEventListener("change", function () {
    if (showPassword.checked) {
        myInput.type = "text";
    } else {
        myInput.type = "password";
    }
});

////////////////////////////////////////////////// login ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// remove_user ////////////////////////////////////////////////////////////

$(document).ready(function () {
    // Load data from server
    $.getJSON('/get_data', function (data) {
        // Sort data alphabetically by description
        data.sort(function (a, b) {
            return a.description.localeCompare(b.description);
        });

        // Populate dropdown with sorted data
        var dropdown = $('#myDropdown');
        $.each(data, function (index, value) {
            var optionText = value.description;
            var optionValue = JSON.stringify(value);
            dropdown.append($('<option>').text(optionText).attr('value', optionValue));
        });

        // Set initial details
        var initialData = data[0];
        displayDetails(initialData);
    });

    // Function to display details when an item is selected
    $('#myDropdown').change(function () {
        var selectedData = JSON.parse($(this).val());
        displayDetails(selectedData);
    });

    function displayDetails(selectedData) {
        $('#details #description').val(selectedData.description);
        $('#details #user_name').val(selectedData.user_name);
        $('#details #user_level').val(selectedData.user_level);

        // Convert user_enable to readable text
        var statusText = selectedData.user_enable === 1 ? 'Active' : 'Inactive';
        $('#Show #status').val(statusText);

        swapDropdownValues(statusText);
    }

    function swapDropdownValues(statusText) {
        var dropdown = $('#myDropdown');
        var activeOption = dropdown.find('option[value="active"]');
        var inactiveOption = dropdown.find('option[value="inactive"]');

        if (statusText === 'Active') {
            activeOption.prop('selected', true);
            inactiveOption.prop('selected', false);
        } else {
            inactiveOption.prop('selected', false);
            activeOption.prop('selected', true);
        }
    }
});


////////////////////////////////////////////////// remove_user ////////////////////////////////////////////////////////////

////////////////////////////////////////////////// site-detail ////////////////////////////////////////////////////////////

$(document).ready(function () {
    // Event listener for region dropdown change
    $('#region_dropdown').change(function () {
        // Get the selected region value
        var selectedRegion = $(this).val();

        // Make an Ajax request to get updated tag options based on the selected region
        $.ajax({
            type: 'GET',
            url: '/get_tags',
            data: { 'selected_region': selectedRegion },
            success: function (response) {
                // Sort tag options alphabetically starting from 'a'
                response.tag_options.sort(function (a, b) {
                    return a.localeCompare(b);
                });

                // Update tag dropdown options
                var tagDropdown = $('#tag_dropdown');
                tagDropdown.empty();
                $.each(response.tag_options, function (index, tagOption) {
                    tagDropdown.append('<option value="' + tagOption + '">' + tagOption + '</option>');
                });
            },
            error: function (error) {
                console.log('Error fetching tag options:', error);
            }
        });
    });
});


function clearFilters() {
    document.getElementById('region_dropdown').value = '';
}

////////////////////////////////////////////////// site-detail ////////////////////////////////////////////////////////////