// class BoggleGame{
//     constructor(boardId, times = 120){
//         this.secs = times;
//         this.score = 0;
//         this.words =[];
//         this.board = $("#" + boardId);

//         // every 1000 msec, "tick"
//         this.timer = setInterval(this.tick.bind(this), 1000);
//     }
// }


const word = document.querySelector("input");
let word_Array = [];
let score = 0;
let score_Array = [];

// button trigger function
$("#submitWords").on('submit', async function (event) {
    event.preventDefault();
    await show_words();
    await add_score();
});

// check if word is ok or not
async function checkWord() {
    let response = await axios.get('/check-word',
        { params: { word: word.value } });
    return response.data;
}

// show words if its okay other than do nothing
async function show_words() {
    let response = await checkWord();
    console.log(response);
    console.log(word.value);
    if (response === "ok") {
        console.log(word.value);
        word_Array.push(word.value);
        $('#words').append($("<li>", { text: word.value }));
    } else if (response === "not-on-board") {
        return
    } else if (response === "not-word") {
        return
    }
}

// score
async function add_score() {
    let response = await checkWord();
    if (response === "ok") {
        score += 1;
        $('#score').text("Score: " + score);
    }
}

// timer countdown

async function countDown(sec) {
    let secs = setInterval(async function () {
        sec--;
        $('#secs').text("Seconds Left: " + sec + "s");
        if (sec <= 0) {
            clearInterval(secs);
            $('#secs').text("Seconds Left: " + 0 +"s");    
            await post_score();        
        } 
    }, 1000);
}

countDown(60);


// send score to server
async function post_score() {
    console.log("score" , score)
    let response = await axios.post('/post-score', { score: score});
    console.log(response.data)
}
