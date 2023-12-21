function confirmDelete() {
    var username = document.getElementById("deleteUsername").value.trim();
    var confirmation = confirm("Are you sure you want to delete the user: " + username + "?");

    if (confirmation) {
        deleteUser(username);
    } else {
        alert("Deletion canceled.");
    }
    resetDeleteForm();
}

function deleteUser(username) {
    // ทำการเรียกใช้ API เพื่อลบผู้ใช้
    fetch('/delete-user', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("User '" + username + "' has been deleted.");
            } else {
                alert("Failed to delete the user.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while deleting the user.");
        });
}

function cancelDelete() {
    alert("Deletion canceled.");
    resetDeleteForm();
}

function resetDeleteForm() {
    document.getElementById("deleteUsername").value = "";
}


fetch('/delete-user/1', {
    method: 'DELETE',
  })
  .then(response => {
    if (response.ok) {
      console.log('User deleted successfully');
    } else {
      console.error('Failed to delete user');
    }
  });
  