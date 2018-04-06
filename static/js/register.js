function checkPasswordMatch() {
    var password = $("#registerPassword").val();
    var confirmPassword = $("#confirmPassword").val();

    if (password != confirmPassword)
        $("#divCheckPasswordMatch").html("Passwords do not match!");
    else
        $("#divCheckPasswordMatch").html("Passwords match.");
}

$(document).ready(function () {
   $("#confirmPassword").keyup(checkPasswordMatch);
});
