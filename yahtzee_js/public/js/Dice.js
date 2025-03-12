console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element=rolls_remaining_element;
        this.dice_elements= dice_elements;
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        console.log(Number(this.rolls_remaining_element.textContent))
        return Number(this.rolls_remaining_element.textContent);
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values(){
        let values = [];
        for (let die of this.dice_elements){
            if (die.src.includes("blank")){
                values.push(0);
            }else if (die.src.includes("one")){
                values.push(1);
            }else if (die.src.includes("two")){
                values.push(2);
            }else if (die.src.includes("three")){
                values.push(3);
            }else if (die.src.includes("four")){
                values.push(4);
            }else if (die.src.includes("five")){
                values.push(5);
            }else if (die.src.includes("six")){
                values.push(6);
            }
        }

        return values;
    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer represenitng the sum of all five dice
    */
    get_sum(){
        let values = this.get_values();
        if (values == [0,0,0,0,0]){
            return 0;
        }
        let sum = values.reduce(function(acc, num){
            return acc+num;
        });
        return sum
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){
        let values = this.get_values();
        let counts = [0,0,0,0,0,0];
        for (let i=0;i<values.length;i++){
            counts[values[i]-1]++;
        }
        return counts;
    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){
        let values = []
        if (Number(document.getElementById("rolls_remaining").innerHTML)>0){
            document.getElementById("rolls_remaining").innerHTML = Number(document.getElementById("rolls_remaining").innerHTML)-1;
            for (let die of this.dice_elements){
                if (die.classList.contains("reserved")){
                    values.push(-1);
                }else{
                    let random_int = Math.floor(Math.random()*6)+1
                    values.push(random_int)
                }
            }
            this.set(values, Number(document.getElementById("rolls_remaining").innerHTML))
            
        }
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        for (let die of this.dice_elements){
            if (die.classList.contains("reserved")){
                die.classList.remove("reserved");
            }
        }
        this.set([0,0,0,0,0], 3);  


    }

    /**
     * Performs all necessary actions to reserve/unreserve a particular die
     * <br> Adds "reserved" as a class label to indicate a die is reserved
     * <br> Removes "reserved" a class label if a die is already reserved
     * <br> Hint: use the classlist.toggle method
     *
     * @param {Object} element the <img> element representing the die to reserve
    */
    reserve(die_element){
        if (die_element.src.includes("blank")){
            console.log("Cannot reserve. Die is blank.")
        }else{
            die_element.classList.toggle("reserved");
        }
    }

    /**
     * A useful testing method to conveniently change dice / rolls remaining
     * <br> A value of 0 indicates that the die should be blank
     * <br> A value of -1 indicates that the die is reserved and should not be updated
     *
     * @param {Array} new_dice_values an array of five integers, one for each die value
     * @param {Number} new_rolls_remaining an integer representing the new value for rolls remaining
     *
    */
    set(new_dice_values, new_rolls_remaining){
       let i=0;
        for (let die of this.dice_elements){
            if (new_dice_values[i] !=-1){
                die.src=`/public/img/${this.photo_names[new_dice_values[this.dice_elements.indexOf(die)]]}.svg`;
            }

            i++;
        }
        this.rolls_remaining_element.textContent = String(new_rolls_remaining);

        document.getElementById("rolls_remaining").innerHTML = new_rolls_remaining;
        // document.getElementById("feedback").innerHTML = ""
        // document.getElementById("feedback").classList.remove("good")
        // document.getElementById("feedback").classList.remove("bad")
        

    }
}


export default Dice;