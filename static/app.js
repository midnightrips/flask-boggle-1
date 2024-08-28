const $userInput = $('#guess');
const $score = $('#score');
const $btn = $('#submit');
const $timer = $('#timer');
const $highscore = $('#highscore');
const $plays = $('#times-played');
const $restart = $('#restart');
let score = 0;
let timer;
let plays = 0;
let highscore = 0;

function startTimer(duration) {

    timer = setTimeout(() => {
        $userInput.prop('disabled', true);
        $btn.prop('disabled', true);
        $('#result').text('Time is up!');
    }, duration * 1000);
}

function startTimer(duration) {
    // Set a timeout to disable input and button after time is up
    let timeLeft = duration;

    timer = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timer);
            $userInput.prop('disabled', true); //https://www.w3schools.com/jquery/html_prop.asp
            $btn.prop('disabled', true);
            $timer.text('Time is up!');
            // $plays.text(`Times played: ${plays}`);
            $restart.show(); //show 'play again' button
            finalScore();
            return;
        }

        $timer.text(`Time left: ${timeLeft} seconds`);
        timeLeft -= 1;
    }, 1000);
}

async function sendGuess(e) {
    e.preventDefault();

    let guess = $userInput.val().trim();
    $userInput.val(''); //clear search bar

    // if (!guess.trim()) {
    //     $('#result').html(`<p>Error: Guess cannot be empty</p>`);
    //     return;
    // }

    const res = await axios.get('http://127.0.0.1:5000/guess', {
        params: { guess },
        headers: {
            'Accept': 'application/json'
        }
    });

    console.log(res.data.result);

    $('#result').text(res.data.result);

    if (res.data.result == 'ok') {
        score += guess.length;
    }

    $score.text(`Current score: ${score}`);

    if (score > highscore) {
        highscore = score;
    }
}

async function finalScore() {
    console.log(score);
    const res = await axios.post('/score', { score, highscore, plays });
    console.log(res.data);
}

$('#submit').on('click', sendGuess);

$(document).ready(() => {
    // Start the timer when the page loads
    startTimer(60);
    // $highscore.text(`Highscore: ${highscore}`);
    // $score.text(`Score: ${score}`);
    $restart.hide();
});
