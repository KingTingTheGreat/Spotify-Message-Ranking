
/**
 * @returns a phone number with all non-numeric characters removed
 * additionally, removes the leading 1 if the phone number is 11 digits long
 */
function cleanPhoneNumber(phone_number) {
    // Remove all non-numeric characters
    phone_number = phone_number.replace(/\D/g, '');
    // assume the user is in the US
    if (phone_number.length === 11 && phone_number[0] === '1') {
        phone_number = phone_number.slice(1);
    }
    // ensure the phone number is 10 digits long
    else if (phone_number.length !== 10) {
        return null;
    }
    return phone_number;
}

/**
 * makes a request to the server to check if the phone number is already in the database
*/
function fetchContainsNumber(number, callback) {
    // api url
    const URL = `http://127.0.0.1:8888/api/contains?phone_number=${number}`;
    // make a request to the url
    fetch(URL)
        .then(response => response.text())
        .then(data => {
            callback(data, null);
        })
        .catch(error => {
            callback(null, error);
        });
}

/**
 * 
 * @returns true if the phone number is already in the database, false otherwise
 */
function submitPhoneNumberOld() {
    const input_number = document.getElementById('phone_number').value;
    const phone_number = cleanPhoneNumber(input_number);
    console.log(`PhoneNumber to check is ${phone_number}`);

    if (phone_number === null) {
        console.log("Please enter a valid phone number.");
        // alert("Please enter a valid phone number.");
        return;
    }
    fetchContainsNumber(phone_number, (data, error) => {
        if (error) {
            console.error("Error:", error);
            // alert("An error occurred. Please try again later.");
        }
        if (data === "true") {
            // alert("This phone number has already been signed up for this service.");
            console.log(data);
            console.log("This phone number has already been signed up for this service.");
        } else if (data == "false") {
            // alert("You have been signed up for this messaging service!");
            console.log(data);
            console.log("Success! You have been signed up for this service.");
        }
        else {
            console.log(data);
            console.log("Error: data is not a boolean value.");
        }
    });
}

function submitPhoneNumber() {
    const inputNumber = document.getElementById('phone_number').value;
    const phoneNumber = cleanPhoneNumber(inputNumber);
    console.log(phoneNumber);
    window.location.href(`http://127.0.0.1:8888/api/signup?phone_number=${phoneNumber}`);
    // fetch(`http://127.0.0.1:8888/api/signup?phone_number=${phoneNumber}`, {
    //     method: 'POST'
    // })
    //     .then(response => response.text())
    //     .then(data => {
    //         console.log(data);
    //     })
    //     .catch(error => {
    //         console.error("Error:", error);
    //     });
}
