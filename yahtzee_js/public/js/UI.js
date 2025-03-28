console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

let socket=io.connect('/')


//-------Dice Setup--------//
display_feedback("New game initiated successfully", "good")
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);


let username = document.getElementById("uname").value
console.log(`Username is ${username}`)

let save_game = document.getElementById("save_game");
save_game.addEventListener('click', save_game_handler)

let load_game = document.getElementById("load_game");
load_game.addEventListener("click", load_game_handler)

let dice_elements =[];
for (let i = 0; i<5; i++){
    let die = document.getElementById("die_"+i);
    die.addEventListener('dblclick', reserve_die_handler);
    dice_elements.push(die);
}
let rolls_remaining_element = document.getElementById("rolls_remaining");

let dice = new Dice(dice_elements, rolls_remaining_element);
window.dice = dice; //useful for testing to add a reference to global window object



//-----Gamecard Setup---------//
let category_elements = Array.from(document.getElementsByClassName("category"));
for (let category of category_elements){
    category.addEventListener('keypress', function(event){
        if (event.key === 'Enter') {
            rolls_remaining_element.innerHTML = parseInt(dice.rolls_remaining_element.innerHTML);
            enter_score_handler(event);
        }
    });
}
let score_elements = Array.from(document.getElementsByClassName("score"));
let gamecard = new Gamecard(category_elements, score_elements, dice);
window.gamecard = gamecard; //useful for testing to add a reference to global window object


//---------Event Handlers-------//
function reserve_die_handler(event){
    console.log("Trying to reserve "+event.target.id);
    dice.reserve(event.target);
}

function roll_dice_handler(){
    if (Number(document.getElementById("rolls_remaining").innerHTML) >0){
        dice.roll();
        document.getElementById("feedback").innerHTML = ""
        document.getElementById("feedback").classList.remove("good")
        document.getElementById("feedback").classList.remove('bad')
    }else{
        display_feedback("ERROR ERROR you do NOT have enough rolls!!!", "bad") 
    }
    // rolls_remaining_element.innerHTML = dice.rolls_remaining_element;
    console.log("Dice values:", dice.get_values());
    console.log("Sum of all dice:", dice.get_sum());
    console.log("Count of all dice faces:", dice.get_counts());
}

function enter_score_handler(event){
    console.log("Score entry attempted for: ", event.target.id, " for ", event.target.value);
    if (dice.get_sum() == 0){
        display_feedback("ERROR ERROR cannot enter a score when dice are blank", "bad")  

    }else if (gamecard.is_valid_score(event.target.id.replace("_input",""), event.target.value)==true){
        event.target.disabled=true;
        gamecard.update_scores();
        display_feedback("Score entered successfully.", "good")
        document.getElementById("rolls_remaining").innerHTML = 3;
        dice.reset()

        
        // since it's valid, emit a socket event valid score
        scorecard = JSON.stringify(Gamecard.to_object()) // get scorecard
        socket.emit("valid_score", {username:username, scorecard:scorecard})
        

    }else{
        display_feedback("Invalid score entered", "bad") 

    }
    if (gamecard.is_finished()==true){
        display_feedback("Scorecard completed!! Hooray.", "good") 
        dice.reset()
        document.getElementById("rolls_remaining").innerHTML = 0;

    }



}

function save_game_handler(event){
    let savedGame = gamecard.to_object()
    localStorage.setItem("yahtzee", JSON.stringify(savedGame));
    display_feedback("Game saved successfully", "good")
    console.log(savedGame)
    
}

function load_game_handler(event){
    let loadedGame = localStorage.getItem("yahtzee")
    if (loadedGame != null){
        let parsedGame =  JSON.parse(loadedGame)
        gamecard.load_scorecard(parsedGame);
        console.log(parsedGame)
        display_feedback("Game loaded successfully", "good")
    }else{
        display_feedback("No game can be loaded", "bad")
    }
    gamecard.update_scores()

    

}


//------Feedback ---------//
function display_feedback(message, context){
    console.log(context, "Feedback: ", message);
    document.getElementById("feedback").innerHTML=message;
    document.getElementById('feedback').classList = context;

}

// socket smile

