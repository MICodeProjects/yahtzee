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
        let check=false;
        let scoreObject = this.to_object();
        Object.keys(scoreObject).forEach(function(section){
            if (section != "rolls_remaining"){
                console.log()
                check = Object.keys(scoreObject[section]).filter(function(category){
                    return document.getElementById(`${category}_input`).disabled==true
                })
            }
            if (check==false){
                return false;
            }
        })
        return true;
        
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
        // check if value is int
        if (this.isNumeric(value)==false){
            return false;
        }

        // setting up
        let scorecard = this.to_object()
        let diceCounts = this.dice.get_counts()

        // upper category
        if (this.dice.photo_names.includes(category)){
            let categoryInd = this.dice.photo_names.indexOf(category);
            let score = diceCounts[categoryInd-1]*categoryInd;
            console.log(categoryInd)
            console.log(`category is ${category}, dice count is ${diceCounts[categoryInd-1]}, should be score is ${score}, and dice number is ${categoryInd}`)
            return score==value;
        }

        // lower category
        if (category == "three_of_a_kind"){
            return ((diceCounts.includes(3) || diceCounts.includes(4) || diceCounts.includes(5)) && this.dice.get_sum() == value)
        }
        if (category == "four_of_a_kind"){
            if ((diceCounts.includes(4) || diceCounts.includes(5)) && this.dice.get_sum() == value){
                return true;
            }
            return false;
        }
        if (category == "yahtzee"){
            return (diceCounts.includes(5) && value==50);
        }
        if (category == "full_house"){
            if (diceCounts.includes(2) && diceCounts.includes(3)){
                return (value==25)
            }
            return false;
        }
        if (category =="large_straight"){
            return ((diceCounts[5]==0 || diceCounts[0]==0)&& value==40);

        }
        // doesnt work
        if (category =="small_straight"){
            let sortedDice = this.dice.get_values().sort();
            console.log("sorted dice ", sortedDice)
            let count = 0;
            for (let i=1;i<sortedDice.length;i++){
                if (sortedDice[i] == sortedDice[i-1]+1){
                    count++;
                }else if (sortedDice[i]!=sortedDice[i-1]){
                    count=0;
                }
                if (count==2){
                    return true;
                }
                
            }
            return false;
            
        }
        if (category =="chance"){
            return (value == this.dice.get_sum())
        }
        

    }



    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){
        let total=0;
        let scorecard = this.to_object();
        for (let category of scorecard.keys()){
            total = total + scorecard[category].reduce(function(acc,curScore){
                if (curScore != -1){
                    return acc + curScore
                }
                return acc;
            })
        }
        return total;
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       let lowerScore=0;
       let upperScore=0;
       let upperBonus=0;

       let scorecard =this.to_object()
       for (category of scorecard){
            if (category == 'lower'){
                lowerScore = scorecard[category].values().reduce(function(acc,cur){
                    if (cur != ''){
                        return acc + parseInt(cur)
                    }
                })
            }else{
                upperScore = scorecard[category].values().reduce(function(acc,cur){
                    if (cur != ''){
                        return acc + parseInt(cur)
                    }
                    return acc
                })

            }
       }
       if (upperScore >63){
           upperBonus=35;
       }
       document.getElementById("upper_score").innerHTML = String(upperScore)
       document.getElementById("upper_bonus").innerHTML = String(upperBonus)
       document.getElementById("upper_total").innerHTML = String(upperScore + upperBonus)

       document.getElementById("lower_score").innerHTML = String(lowerScore)
       document.getElementById("upper_total_lower").innerHTML = String(upperScore);
       document.getElementById("grand_total").innerHTML = String(upperScore + upperBonus + lowerScore);
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
        Object.keys(score_info).forEach(function(section){
            if (section != "rolls_remaining"){
                Object.keys(score_info[section]).forEach(function(category){
                    console.log(`Section: ${section}, category: ${category}, value: ${score_info[section][category]}`)
                    document.getElementById(`${category}_input`).value = score_info[section][category];
                    document.getElementById(`${category}_input`).disabled = true;

                })
            }else{
                document.getElementById("rolls_remaining").innerHTML = score_info["rolls_remaining"]
            }
        })
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



    to_object(){
        let scorecardObject = {};
        scorecardObject["rolls_remaining"] = this.dice.get_rolls_remaining()

        let lowerCard = document.getElementsByClassName("lower");
        let upperCard = document.getElementsByClassName("upper");
        scorecardObject["lower"] = {};
        scorecardObject["upper"] = {};
        for (let card of upperCard){

            scorecardObject["lower"][card.id.replace("_input","")] = card.value;
        }
        for (let card of lowerCard){

            scorecardObject["upper"][card.id.replace("_input","")] = card.value;
        }


        console.log(scorecardObject);
        return scorecardObject;
    }

    isNumeric(scoreInput) {
        if (isNaN(scoreInput) == false && isNaN(parseInt(scoreInput))==false && String(scoreInput).includes('.')==false){
            return true;
        }
        return false;
    }
}

export default Gamecard;