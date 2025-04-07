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
    is_finished(username){
        let scoreObject = Object.keys(this.to_object(username)["upper"]).concat(Object.keys(this.to_object(username)["lower"]));
        console.log(scoreObject)
        return scoreObject.every(function(category){
            console.log(category, document.getElementById(`${category}_input_${username}`).disabled)
            if (document.getElementById(`${category}_input_${username}`).disabled==true){
                return true;
            }
            return false;
        },0)
           
        
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
    is_valid_score(category, value, username){
        // check if value is int
        if (this.isNumeric(value)==false){
            return false;
        }

        // check if value is 0 (always valid score)
        if (value==0){
            return true;
        }

        // setting up
        let scorecard = this.to_object(username)
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
    get_score(username){
        let total = 0;

 
        let scorecard =this.to_object(username)
        // Upper
        let upperScore = Object.keys(scorecard["upper"]).reduce(function(acc,category){
            console.log(category, acc)
            if (document.getElementById(`${category}_input_${username}`).disabled==true){
                return acc + Number(document.getElementById(`${category}_input_${username}`).value)
            }
            return acc;
        },0)

            // bonus check
            if (upperScore > 63){
                upperScore+=35;
            }
            
        // LOWER
        let lowerScore = Object.keys(scorecard["lower"]).reduce(function(acc,category){
            console.log(category, acc)
            if (document.getElementById(`${category}_input_${username}`).disabled==true){
                return acc + Number(document.getElementById(`${category}_input_${username}`).value)
            }
            return acc
        },0)
                   
        return total+lowerScore+upperScore;
    }

    

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(username){
       let lowerScore=0;
       let upperScore=0;
       let upperBonus="";

       let scorecard =this.to_object(username)
       // Upper
        upperScore = Object.keys(scorecard["upper"]).reduce(function(acc,category){
            console.log(category, acc)
            if (document.getElementById(`${category}_input_${username}`).disabled==true){
                return acc + Number(document.getElementById(`${category}_input_${username}`).value)
            }
            return acc;
        },0)

        // bonus check
        if (upperScore > 63){
            upperBonus=35;
        }
        
    // LOWER
        lowerScore = Object.keys(scorecard["lower"]).reduce(function(acc,category){
            console.log(category, acc)
            if (document.getElementById(`${category}_input_${username}`).disabled==true){
                return acc + Number(document.getElementById(`${category}_input_${username}`).value)
            }
            return acc
        },0)

       document.getElementById(`upper_score_${username}`).innerHTML = String(upperScore)
       document.getElementById(`upper_bonus_${username}`).innerHTML = String(upperBonus)
       if (upperBonus != ""){
            upperScore = upperScore + upperBonus
       }
        document.getElementById(`upper_total_${username}`).innerHTML = String(upperScore)
       

       document.getElementById(`lower_score_${username}`).innerHTML = String(lowerScore)
       document.getElementById(`upper_total_lower_${username}`).innerHTML = String(upperScore);
       document.getElementById(`grand_total_${username}`).innerHTML = String(upperScore + lowerScore);
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
    load_scorecard(score_info, username){
        let names = ["upper", "lower", "rolls_remaining"]
        names.forEach(function(section){
            if (section != `rolls_remaining`){
                Object.keys(score_info[section]).forEach(function(category){
                    if (score_info[section][category] == -1){
                        document.getElementById(`${category}_input_${username}`).value = "";
                        document.getElementById(`${category}_input_${username}`).disabled = false;

                    }else{
                        document.getElementById(`${category}_input_${username}`).value = score_info[section][category];
                        document.getElementById(`${category}_input_${username}`).disabled = true;
                    }

                })
            }else{
                document.getElementById(`rolls_remaining`).innerHTML = score_info["rolls_remaining"]
            }
        })
        this.update_scores(username);
    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":3,
                "two":5,
                "three":20,
                "four":19,
                "five":30,
                "six":1
            },
            "lower":{
                "three_of_a_kind":6,
                "four_of_a_kind":3,
                "full_house":0,
                "small_straight":4,
                "large_straight":23,
                "yahtzee":50,
                "chance":2
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */



    to_object(username){
        let scorecardObject = {
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
        scorecardObject["rolls_remaining"] = Number(document.getElementById(`rolls_remaining`).innerHTML)
        
        for (let category in scorecardObject.upper){
                    if (document.getElementById(`${category}_input_${username}`).disabled == false || document.getElementById(`${category}_input_${username}`).value == ""){
                        scorecardObject["upper"][category] =-1
                    }else {
                        scorecardObject["upper"][category] = Number(document.getElementById(`${category}_input_${username}`).value);
                    }
                }
        for (let category in scorecardObject.lower){
                    if (document.getElementById(`${category}_input_${username}`).disabled == false || document.getElementById(`${category}_input_${username}`).value == ""){
                        scorecardObject["lower"][category] =-1
                    }else {
                        scorecardObject["lower"][category] = Number(document.getElementById(`${category}_input_${username}`).value);
                    }
                }


        return scorecardObject;



        // let scorecardObject = {};
        // scorecardObject["rolls_remaining"] = Number(document.getElementById("rolls_remaining").innerHTML)
        

        // let lowerCard = document.getElementsByClassName("lower category");
        // let upperCard = document.getElementsByClassName("upper category");
        // scorecardObject["lower"] = {};
        // scorecardObject["upper"] = {};
        // for (let card of upperCard){
        //     if (card.disabled == false || card.value == ""){
        //         scorecardObject["upper"][card.id.replace("_input","")] =-1
        //     }else {
        //         scorecardObject["upper"][card.id.replace("_input","")] = Number(card.value);
        //     }
        // }
        // for (let card of lowerCard){
        //     if (card.disabled == false || card.value == ""){
        //         scorecardObject["lower"][card.id.replace("_input","")] =-1
        //     }else {
        //         scorecardObject["lower"][card.id.replace("_input","")] = Number(card.value);
        //     }
        // }


        // return scorecardObject;
    }

    isNumeric(scoreInput) {
        if (isNaN(scoreInput) == false && isNaN(parseInt(scoreInput))==false && String(scoreInput).includes('.')==false){
            return true;
        }
        return false;
    }
}

export default Gamecard;