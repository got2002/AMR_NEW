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