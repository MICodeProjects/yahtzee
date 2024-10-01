class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements;
        this.dice=myDice;
        this.score_elements=score_elements;
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
    
    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){
        let scorecard = this.to_object()
        let diceCounts = this.dice.getCounts()
        if (scorecard["upper"].keys().includes(category)){
            let categoryInd = this.dice.photo_names().indexOf(category);
            let score = diceCounts[categoryInd]*categoryInd;
            console.log(category, diceCounts[categoryInd], score)
            return score==value;
        }
        if (category == "three_of_a_kind"){
            return this.xOfAKind(3).includes(value)
        }
        if (category == "four_of_a_kind"){
            return this.xOfAKind(4).includes(value)
        }
        if (category == "yahtzee"){
            return this.xOfAKind(5).includes(value)
        }
        if (category == "full_house"){
            if (diceCounts.includes(2) && diceCounts.includes(3)){
                return (value==this.dice.get_sum())
            }
        }
        if (category =="large_straight"){
            return value == 1+2+3+4+5+6;
        }
        if (category =="small_straight"){
            return [2] == diceCounts.filter(function(die){
                return (die != 1);
            })
        }
        if (category =="chance"){
            return (value == this.dice.get_sum())
        }
        

    }

    xOfAKind(freq){
        let possibleScores = this.dice.getCounts.map(function(elt, die){
            if (elt >=freq){
                return freq*die
            }
            return -1
        });
        return possibleScores;
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){
        // let total=0;
        // let scorecard = this.to_object();
        // for (let category of )
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       
    }

    /**
     * Loads a scorecard from a JS object in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(score_info){
       
    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */

    isNumeric(scoreInput) {
        if (isNaN(scoreInput == false && isNaN(parseFloat(scoreInput)==false))){
            return true;
        }
    }

    to_object(){
        let scorecardObject = {};
        scorecardObject["rolls_remaining"] = this.dice.get_rolls_remaining()

        let lowerCard = document.getElementsByClassName("lower");
        let upperCard = document.getElementsByClassName("upper");
        scorecardObject["lower"] = {};
        scorecardObject["upper"] = {};
        for (let card of upperCard){
            let val = -1;
            if (this.isNumeric(card.value)){
                val = parseInt(card.value)
            }
            scorecardObject["upper"][card.id.replace("_input","")] = val;
        }
        for (let card of lowerCard){
            let val = -1;
            if (this.isNumeric(card.value)){
                val = card.value;
            }
            scorecardObject["lower"][card.id.replace("_input","")] = val;
        }


        console.log(scorecardObject);
        return scorecardObject;
    }
}

export default Gamecard;





