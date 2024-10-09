console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

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
    display_feedback("Rolling the dice...", "good");
    dice.roll();
    // rolls_remaining_element.innerHTML = dice.rolls_remaining_element;
    console.log("Dice values:", dice.get_values());
    console.log("Sum of all dice:", dice.get_sum());
    console.log("Count of all dice faces:", dice.get_counts());
}

function enter_score_handler(event){
    let feedback = document.getElementById("feedback")
    console.log("Score entry attempted for: ", event.target.id, " for ", event.target.value);
    if (gamecard.is_valid_score(event.target.id.replace("_input",""), event.target.value)==true){
        event.target.disabled=true;
        gamecard.update_scores();
        feedback.classList.add("green")
        feedback.classList.remove('red')

        if (gamecard.is_finished()==true){
            feedback.innerHTML = "Scorecard completed 🥳"
        }else{
            feedback.innerHTML = "Valid score entered 😁"
        }

    }else{

        event.target.value = "";
        feedback.classList.add("red")
        feedback.classList.remove('green')
        feedback.innerHTML = "Invalid score entered"       
    }
}

function save_game_handler(event){
    gamecard.
}

function load_game_handler(event){

}


//------Feedback ---------//
function display_feedback(message, context){
    console.log(context, "Feedback: ", message);

}