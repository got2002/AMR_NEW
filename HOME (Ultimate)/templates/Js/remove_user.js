function updateTime() {
    const today = new Date();
    const date = today.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const time = today.toLocaleTimeString();
    document.getElementById('datetime').innerHTML = `${date} - ${time}`;
}

updateTime();
setInterval(updateTime, 1000);

window.onclick = function (event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
                openDropdown.previousElementSibling.classList.remove('active');
            }
        }
    }
}

// Function to toggle dropdown visibility
function toggleDropdown(dropdown) {
    var content = dropdown.nextElementSibling;
    if (content.style.display === 'block') {
        content.style.display = 'none';
        dropdown.classList.remove('active');
    } else {
        content.style.display = 'block';
        dropdown.classList.add('active');
    }
}

//* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
    dropdown[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var dropdownContent = this.nextElementSibling;
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    });
}

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

        // สลับค่าใน Dropdown เมื่อแสดงรายละเอียด
        swapDropdownValues(statusText);
    }

    function swapDropdownValues(statusText) {
        var dropdown = $('#myDropdown');
        var activeOption = dropdown.find('option[value="active"]');
        var inactiveOption = dropdown.find('option[value="inactive"]');

        // สลับค่าใน Dropdown
        if (statusText === 'Active') {
            activeOption.prop('selected', true);
            inactiveOption.prop('selected', false);
        } else {
            inactiveOption.prop('selected', false);
            activeOption.prop('selected', true);
        }
    }
});
