console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= Number(rolls_remaining_element);
        this.dice_elements= dice_elements;
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return this.rolls_remaining_element;
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
            console.log(die.src)
        }

        console.log("Values are: ", values);
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
        if (this.rolls_remaining_element>0){
            this.rolls_remaining_element--;
            for (let die of this.dice_elements){
                if (die.classList.contains("reserved")){
                    continue;
                }else{
                    let min = Math.ceil(1);
                    let max = Math.floor(5);
                    let random_int = Math.floor(Math.random() * (max - min + 1)) + min;
                    die.src=`/img/${this.photo_names[random_int]}.svg`;
                }
            }
        }
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        for (let die of this.dice_elements){
            die.src="/img/blank.svg";
            if (die.classList.contains("reserved")){
                die.classList.remove("reserved");
            }
        }
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
        let die = document.getElementById(die_element)
        die.classList.toggle("reserved");
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
        for (let i=0;i<this.dice_elements.length;i++){
            this.dice_elements[i].src=`/img/${new_dice_values[i]}.svg`;
        }
        this.rolls_remaining_element=new_rolls_remaining
    }
}

export default Dice;