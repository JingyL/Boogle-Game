class BoggleGame {
    constructor(times = 60) {
        this.secs = times;
        this.score = 0;
        this.words = [];
        this.board = $("#table");
        // button trigger function
        $('#submitWords').on('submit', this.triggerFunctions.bind(this));
    }

    // trigger the submit button and operate other functions
    async triggerFunctions(event) {
        event.preventDefault();
        await this.checkWord();
        if (this.secs === 0) {
            $("#msg").text(" Out of time!!!");
            return;
        }
        await this.show_words();
        this.add_score();
    }

    // check if word is ok or not
    async checkWord() {
        const word = $('.guessword').val();
        console.log(word)
        console.log("time", this.secs)
        let response = await axios.get('/check-word',
                { params: { word: word } });
        let result = response.data;
        if (result === "ok") {
            if(this.words.includes(word)){
                $("#msg").text("The word has already existed");
            }else{
                this.words.push(word);
                console.log( this.words)
            }
        } else if (result === "not-on-board") {
            return
        } else if (result === "not-word") {
            return
        }
    }

    // show words if its okay other than do nothing
    async show_words() {
        let lastIdx = this.words.length - 1;
        let word = this.words[lastIdx]
        $('ul').append($("<li>", { text: word}));
    }

    // score
   add_score() {
            this.score = this.words.length;
            $('#score').text("Score: " + this.score);
    }

    // timer countdown

    async countDown(sec) {
        let game = this;
        let secs = setInterval(async function () {
            sec--;
            game.secs=sec;
            $('#secs').text("Seconds Left: " + sec + "s");
            if (sec <= 0) {
                clearInterval(secs);
                $('#secs').text("Seconds Left: " + 0 + "s");
                await game.post_score();
            }
        }, 1000);
    }


    // send score to server
    async post_score() {
        console.log("score", this.score)
        let response = await axios.post('/post-score', { score: this.score });
        console.log(response.data)
    }


}