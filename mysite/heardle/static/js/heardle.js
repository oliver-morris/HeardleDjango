
function playSound() {
    var number = getNumberShown();
    if (number > 5) {
        number = 5;
    }
    //document.getElementById(`audio${number}`).play();
    var clip = '../' + clips[number];
    //clip = decodeURIComponent(clip);
    var audio = new Audio(clip);
    audio.play();
}

function filterFunction(e) {
    if (e.keyCode == 27) {
      clear();
    } else if (e.keyCode == 13) {
      submit();
    }
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    class_array = document.getElementById("myDropdown").classList;
    if (input.value == "") {
        if (class_array.contains("show")) {
            document.getElementById("myDropdown").classList.remove("show");
        }
    } else {
        if (!class_array.contains("show")) {
            document.getElementById("myDropdown").classList.add("show");
        }
    }
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    var song_names = tracks;
    song_names.sort(function (a, b) {
        if (a < b) {
            return -1;
        }
        if (a > b) {
            return 1;
        }
        return 0;
    })
    a = song_names;
    var new_array = []
    for (i = 0; i < a.length; i++) {
        txtValue = a[i];
        //if (txtValue.toUpperCase().indexOf(filter) > -1) {
        //a[i].style.display = "";
        //} else {
        ////a[i].style.display = "none";
        //}
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            new_array.push(txtValue);
        }
    }
    showSongs(new_array);
}

function showSongs(songs_list) {
    var song_html = ``;
    for (let i = 0; i < songs_list.length; i++) {
        song_html += `
        <p class="song">${songs_list[i]}</p>`;
    }
    document.getElementById("myDropdown").innerHTML = song_html;
    let songs = document.getElementsByClassName("song");
    for (let i in songs) {
        try {
            songs[i].addEventListener("click", selectSong);
        } catch (err) {
            break;
        }
    }
}

function selectSong() {
    var guess = this.innerHTML;
    document.getElementById("myInput").value = guess;
    document.getElementById("myDropdown").classList.remove("show");
}

function submit() {
    var number = getNumberShown();
    var input = document.getElementById("myInput");
    input = input.value;
    var record = document.getElementById("myRecord");
    record = record.value;
    var answer = song;

    const song_names = tracks;
    const lowercased = song_names.map(song_names => song_names.toLowerCase());

    if (lowercased.indexOf(input.toLowerCase()) == -1) {
    return;
    }
    document.getElementById(`lyric${getNumberShown()+1}`).textContent = input;
    if (input.toLowerCase() == answer.toLowerCase()) {
    document.getElementById("myRecord").textContent += "🟩";
    document.getElementById(`lyric${getNumberShown()}`).style.backgroundColor = "green";
    document.getElementById(`lyric${getNumberShown()}`).style.opacity = 0.5;
    return endGame(true);
    } else if (number >= 5) {
    document.getElementById("myRecord").textContent += "🟥";
    document.getElementById(`lyric${getNumberShown()}`).style.backgroundColor = "red";
    document.getElementById(`lyric${getNumberShown()}`).style.opacity = 0.5;
     return endGame(false);
    } else {
      document.getElementById("myRecord").textContent += "🟥";
      document.getElementById(`lyric${getNumberShown()}`).style.backgroundColor = "red";
      document.getElementById(`lyric${getNumberShown()}`).style.opacity = 0.5;
      //setLyric();
      clear();
    }
}

function skip() {
    var number = getNumberShown();
    if (number >= 5) {
    document.getElementById("myRecord").textContent += "⬛";
    document.getElementById(`lyric${getNumberShown()}`).style.backgroundColor = "black";
    document.getElementById(`lyric${getNumberShown()}`).style.opacity = 0.8;
    document.getElementById(`lyric${getNumberShown()}`).textContent = "Skipped";
    return endGame(false);
    }
    document.getElementById("myRecord").textContent += "⬛";
    document.getElementById(`lyric${getNumberShown()}`).style.backgroundColor = "black";
    document.getElementById(`lyric${getNumberShown()}`).style.opacity = 0.8;
    document.getElementById(`lyric${getNumberShown()}`).textContent = "Skipped";
    //setLyric();
    clear();
}

function getNumberShown() {
    var score = document.getElementById("myRecord").textContent;
    var count = 0;
    for (let i = 0; i < score.length; i++) {
    if (score[i] != "⬛") {
        count += 0.5;
    } else {
        count += 1;
    }
    }
    return count-1;
}

function clear() {
    var input = document.getElementById("myInput");
    input.value = "";
    document.getElementById("myDropdown").classList.remove("show");
}

function endGame(success) {
    var lyric_string = "";
    document.getElementById("myDropdown").classList.remove("show");
    document.getElementById('submit').removeAttribute('onclick');
    document.getElementById('skip').removeAttribute('onclick');
    document.getElementById("myInput").type = "hidden";
    var answer = song
    //var lyrics = song
    //document.getElementById("background").innerHTML += `<div id="myInput">${answer}</div>`
    let endScreen = document.querySelector(".level-end");
    endScreen.innerHTML += `${answer}
    <div id="play-again">Play Again</div>
    <div id="close-icon" onClick="minimise()">X</div>`;
                setTimeout(()=>endScreen.classList.add("top"), 500);
                setTimeout(()=>endScreen.style.top = "12%", 500);
                let playAgainButton = document.getElementById("play-again");
                playAgainButton.addEventListener("click", playAgain);
}

function setLyric() {
    var lyrics = JSON.parse(`<?php echo $_COOKIE["lyrics"]; ?>`);
    var number = getNumberShown();
    var lyric_id = `lyric${number+1}`;
    var line = lyrics[number];
    document.getElementById(lyric_id).textContent = line;
}

function minimise() {
    let endScreen = document.querySelector(".level-end");
    endScreen.classList.remove("top")
    endScreen.style.top = "-150%"
    var answer = `<?php echo $_COOKIE["answer"]; ?>`;
    document.getElementById("background").innerHTML += `<div id="myInput">${answer}</div>
    <div id="play-again-minimise">Play Again</div>`
    let playAgainButton = document.getElementById("play-again-minimise");
    playAgainButton.addEventListener("click", playAgain);
}

function playAgain() {
    window.location.href = "/";
}

const song = data["song"]
const tracks = data["tracks"]
const clips = data["clips"]
const artist = data["artist"]

