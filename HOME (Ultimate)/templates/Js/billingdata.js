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
    // แสดง loading overlay
    document.getElementById('loadingOverlay').style.display = 'block';
}


// JavaScript เพื่อแสดงหรือซ่อน div
var None = document.getElementById("None");

// เรียกใช้ฟังก์ชันเพื่อแสดงหรือซ่อน div
function toggleDiv() {
    if (None.style.display === "none") {
        None.style.display = "block";
    } else {
        None.style.display = "none";
    }
}

// เรียกใช้ toggleDiv() เมื่อต้องการเปลี่ยนแปลงสถานะ
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
    // แสดง loading overlay
    document.getElementById('loadingOverlay').style.display = 'block';
}

// ฟังก์ชันนี้ควรถูกเรียกเมื่อข้อมูลถูกโหลดแล้ว
function hideLoading() {
    // ซ่อน loading overlay
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