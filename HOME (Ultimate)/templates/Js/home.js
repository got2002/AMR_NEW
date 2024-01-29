// Object หรือ Class สำหรับการจัดการหน้าเว็บ
const WebManager = {
    updateTime: function () {
        const today = new Date();
        const date = today.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        const time = today.toLocaleTimeString();
        document.getElementById('datetime').innerHTML = `${date} - ${time}`;
    },

    toggleDropdown: function (dropdown) {
        var content = dropdown.nextElementSibling;
        if (content.style.display === 'block') {
            content.style.display = 'none';
            dropdown.classList.remove('active');
        } else {
            content.style.display = 'block';
            dropdown.classList.add('active');
        }
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

// เริ่มต้นการทำงานของ WebManager
WebManager.init();
