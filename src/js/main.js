
function fetchContainsNumber(number, callback) {
    const URL = `http://127.0.0.1:8888/contains?phone_number=${number}`;

    fetch(URL)
        .then(response => response.text())
        .then(data => {
            callback(data, null);
        })
        .catch(error => {
            callback(null, error);
        });
}

function containPhoneNumber() {
    const phone_number = document.getElementById('phone_number').value;
    console.log(`PhoneNumber to check is ${phone_number}`);

    fetchContainsNumber(phone_number, (data, error) => {
        if (error) {
            console.error("Error:", error);
            // alert("An error occurred. Please try again later.");
        }
        if (data === "true") {
            // alert("This phone number has already been signed up for this service.");
            console.log(data);
            console.log("This phone number has already been signed up for this service.");
        } else {
            // alert("You have been signed up for this messaging service!");
            console.log(data);
            console.log("Success! You have been signed up for this service.");
        }
    });

}

