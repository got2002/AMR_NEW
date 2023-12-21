<!-- เพิ่มส่วนนี้เพื่อใช้ Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<!-- เพิ่มส่วนนี้ใน script -->
<script>
    document.addEventListener('DOMContentLoaded', function () {
        // เรียกใช้ฟังก์ชันสร้าง Line Chart เมื่อหน้าเว็บโหลดเสร็จ
        createLineChart();
    });

    function createLineChart() {
        // ดึงข้อมูลจากตาราง HTML
        var table = document.getElementById('searchTable');
        var rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        // สร้างข้อมูลสำหรับ Chart.js
        var chartData = {
            labels: [],  // ตำแหน่งแต่ละแถว
            datasets: [
                {
                    label: 'CORRECTED',
                    data: [],  // ข้อมูลที่จะแสดงในกราฟ
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'UNCORRECTED',
                    data: [],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Pressure',
                    data: [],
                    borderColor: 'rgba(255, 205, 86, 1)',
                    borderWidth: 2,
                    fill: false
                },
                {
                    label: 'Temperature',
                    data: [],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2,
                    fill: false
                }
            ]
        };

        // วนลูปเพื่อดึงข้อมูลจากตารางและเพิ่มลงใน chartData
        for (var i = 0; i < rows.length; i++) {
            var cells = rows[i].getElementsByTagName('td');
            chartData.labels.push(cells[0].textContent);  // ในกรณีที่ตำแหน่งข้อมูลอยู่ในคอลัมน์แรก

            for (var j = 1; j < cells.length; j++) {
                chartData.datasets[j - 1].data.push(parseFloat(cells[j].textContent));
            }
        }

        // สร้าง Line Chart
        var ctx = document.getElementById('lineChart').getContext('2d');
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    },
                    y: {
                        min: 0
                    }
                }
            }
        });
    }
</script>
