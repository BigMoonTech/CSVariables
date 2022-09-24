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

// function to disable the submit button onSubmit and is called in the form tag when "onSubmit" is triggered
function disableSubmit() {
    document.getElementById("submit").disabled = true;
}


// do this stuff as soon as the page loads
$(document).ready(function () {

    // make the dropdown-toggle tabbable
    $("#dropdown-toggle")
        .attr("tabindex", 0)
        .keypress((evt) => {
            const key = evt.key;
            evt.preventDefault();                  // Ensure all default keypress
                                                   // actions are not used
            if (key === ' ' || key === 'Enter') {  // Only send click events for Space or Enter
                evt.currentTarget.click();         // Run the click event for element
            }
        });

    // if the query-area is focused, move focus to the id "query" input field
    // (instead of tabbing to the div, will tab to the input field)
    $("#query-area")
        .focus(() => {
            $("#query").focus();
        });

    // select query input field
    $("#query")
        // if "query" is focused, add the class "ta-focus" to the query area div
        .focus(() => {
            $("#query-area").addClass("ta-focus");
        })
        // or remove the ta-focus class
        .blur(() => {
            $("#query-area").removeClass("ta-focus");
        })

        // if "Enter" pressed in "query", submit the form by clicking the submit button
        .keypress((evt) => {
                const key = evt.key;
                if (key === 'Enter') {
                    evt.preventDefault();
                    document.getElementById("submit").click();
                }
            }
        );

    $("#output")
        // if "output" is focused, add the class "ta-focus" to the output div
        .focus(() => {
            $("#output").addClass("ta-focus");
        })
        // or remove the ta-focus class
        .blur(() => {
            $("#output").removeClass("ta-focus");
        });
});

// jquery animation to show the dropdown menu
$(document).ready(function () {
    $("#dropdown-toggle").click(function () {
        $("#dropdown-menu").slideToggle(330);
    });
});

// close the dropdown menu when the user clicks outside it
document.addEventListener("click", function (event) {
    // if the element "dropdown-toggle" exists:
    if (document.getElementById("dropdown-toggle")) {
        const isClickInside = document.getElementById("dropdown-toggle").contains(event.target);

        // jquery slideUp the dropdown
        if (!isClickInside) {
            $("#dropdown-menu").slideUp();
        }
    }
});


