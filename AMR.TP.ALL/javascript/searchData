
    function searchData() {
        var inputRegion = document.getElementById('inputRegion').value;
        var inputSite = document.getElementById('inputSite').value;
        var selectedDate = document.getElementById('datepicker').value;

        if (inputRegion && inputSite && selectedDate) {
            document.getElementById('warningContainer').style.display = 'none';
            document.getElementById('loadingOverlay').style.display = 'flex';

            // เพิ่มการเรียก API หรือการทำงานด้วยข้อมูลที่ค้นหา
            // เปลี่ยน URL_API เป็น URL ของ API ที่คุณใช้

            var url = `URL_API?region=${inputRegion}&site=${inputSite}&date=${selectedDate}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loadingOverlay').style.display = 'none';
                    displaySearchResults(data);
                })
                .catch(error => {
                    document.getElementById('loadingOverlay').style.display = 'none';
                    console.error('Error:', error);
                    alert('Error occurred during the search. Please try again.');
                });
        } else {
            document.getElementById('warningContainer').style.display = 'block';
        }
    }

    function clearForm() {
        document.getElementById('inputRegion').value = '';
        document.getElementById('inputSite').value = '';
        document.getElementById('datepicker').value = '';

        document.getElementById('warningContainer').style.display = 'none';
        document.getElementById('searchedRegion').textContent = '';
        document.getElementById('searchedSite').textContent = '';
        document.getElementById('searchedDate').textContent = '';

        // เคลียร์ตารางผลลัพธ์การค้นหา
        var tableBody = document.querySelector('.styled-table tbody');
        tableBody.innerHTML = '';
    }

