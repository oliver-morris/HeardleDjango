function searchFunction(event) {
    if (event.keyCode == 13) {
        submit();
    }
}

function submit() {
    input = document.querySelector(".homepage-input");
    artist_input = input.value
    if (artist_input) {
        window.location = "heardle?artist=" + artist_input;
    }
}