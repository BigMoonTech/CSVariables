function countChars() {
    // select the input field with id="variable_query
    const querySelector = document.querySelector("#query");

    // get the count of the number of characters in the input field
    const length = querySelector.value.length;

    // select the span with id="char_count"
    let charCount = document.getElementById("char_count");

    // set the text of the span to the number of characters in the input field in the format "x / 200"
    charCount.textContent = `${length} / 200`;

    // if the number of characters in the input field is greater than 200 add a red border to the input field
    if (length > 200) {
        querySelector.classList.add("text-danger");
        querySelector.classList.add("border-danger");
        charCount.classList.add("text-danger");
    } else {
        querySelector.classList.remove("text-danger");
        querySelector.classList.remove("border-danger");
        charCount.classList.remove("text-danger");
    }
}
