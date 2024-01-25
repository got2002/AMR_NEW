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