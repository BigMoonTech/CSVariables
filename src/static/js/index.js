function countChars() {
    // select the input field with id="variable_query
    const variableQuery = document.querySelector("#variable_query");

    // get the count of the number of characters in the input field
    const variableQueryLength = variableQuery.value.length;

    // select the span with id="char_count"
    let charCount = document.getElementById("char_count");

    // set the text of the span to the number of characters in the input field in the format "x / 200"
    charCount.textContent = `${variableQueryLength} / 200`;

    // if the number of characters in the input field is greater than 200 add a red border to the input field
    if (variableQueryLength > 200) {
        variableQuery.classList.add("text-danger");
        variableQuery.classList.add("border-danger");
        charCount.classList.add("text-danger");
    } else {
        variableQuery.classList.remove("text-danger");
        variableQuery.classList.remove("border-danger");
        charCount.classList.remove("text-danger");
    }
}

// get the client's IP address
let client_ = "";
$.getJSON("https://api.ipify.org?format=json", function (data) {
    // set the P element with id="ip" to the client's IP address
    client_ = data.ip;
    $("#usr_data").text(data.ip);
});