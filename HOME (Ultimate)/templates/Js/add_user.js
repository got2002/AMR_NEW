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

function updateTime() {
    const today = new Date();
    const date = today.toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
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