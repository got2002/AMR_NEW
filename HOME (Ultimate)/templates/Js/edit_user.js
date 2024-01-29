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