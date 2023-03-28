from flask import Flask
from flask import request
from flask import render_template

import bottraining as bt

app = Flask(__name__)

@app.route("/")
def index():
    return (
        """<form method="POST" action="/submit">
            <label for="num_decks">Enter number of decks:</label>
            <input type="number" id="num_decks" name="num_decks" min="1">

            <label for="typical_settings">Do you want to use typical amount of initial dealt cards (2 cards per player) and blackjack winning points (sum of 21)?</label>
            <select id="typical_settings" name="typical_settings">
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>

            <div id="custom_settings" style="display:none;">
              <label for="initial_dealt_cards">Enter the number of initial dealt cards:</label>
              <input type="number" id="initial_dealt_cards" name="initial_dealt_cards" min="1" value="2"><br>

              <label for="winning_points">Enter the number of winning points for blackjack:</label>
              <input type="number" id="winning_points" name="winning_points" min="1" value="21">
            </div>

            <label for="hit_or_stand">Select the dealer's strategy:</label>
            <select id="hit_or_stand" name="hit_or_stand">
              <option value="18">Dealer hits on soft 17</option>
              <option value="17">Dealer stands on soft 17</option>
            </select>

            <label for="double_cards">What cards are you permitted to double?</label>
            <select id="double_cards" name="double_cards">
              <option value="1">Any 2 cards</option>
              <option value="2">9, 10 &amp; 11 only</option>
              <option value="3">10 &amp; 11 only</option>
            </select>

            <button type="submit">Submit</button>
          </form>


            <script>
              // Show/hide custom settings based on user input
              document.querySelector('#typical_settings').addEventListener('change', function() {
                if (this.value === 'no') {
                  document.querySelector('#custom_settings').style.display = 'block';
                } else {
                  document.querySelector('#custom_settings').style.display = 'none';
                }
              });
            </script>"""
    )

@app.route("/submit", methods=["POST"])
def submit():
    number_of_decks = int(request.form['num_decks'])
    doubleVariation = int(request.form['double_cards'])
    dealerCriticalPointsToStick = int(request.form['hit_or_stand'])
    initialNumberOfCard = request.form['initial_dealt_cards']
    if initialNumberOfCard.isdigit():
        initialNumberOfCard = int(initialNumberOfCard)
    else:
        initialNumberOfCard = 2

    winningPoints = request.form['winning_points']

    if winningPoints.isdigit():
        winningPoints = int(winningPoints)
    else:
        winningPoints = 21




    # cards for one deck game
    defaultDeckContent = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                          '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                          '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                          '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']


    DeckContent = []
    for item in defaultDeckContent:
      DeckContent += [item]*number_of_decks


    # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL = bt.TrainAndTestGameBot(100000, 100000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS = bt.TrainAndTestGameBot(100000, 100000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC = bt.TrainAndTestGameBot(100000, 100000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)

    # lambda function for determine hit, stick, or double
    HitStickOrDouble = lambda hitQ, stickQ, doubleQ: "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"


    # report strategy result

    result = ""
    for i in range(0, winningPoints*3-17):
        result += " "
    result +="Q-learning"
    result += "<br>"

    result +="              player (usable ace)"
    for i in range(0, winningPoints*3-36):
        result +=" "
    result +="player (no usable ace)<br>"

    result +="         "
    for p in range(11, winningPoints+1):
        result += str(p)
    result +="             "
    for p in range(11, winningPoints+1):
        result += str(p)
    result += "<br>"

    for d in range (1,11):
        if (d == 10):
            result +="      10   "
        elif (d == 3):
            result +="    D  3   "
        elif (d == 4):
            result +="    e  4   "
        elif (d == 5):
            result +="    a  5   "
        elif (d == 6):
            result +="    l  6   "
        elif (d == 7):
            result +="    e  7   "
        elif (d == 8):
            result +="    r  8   "
        else:
            result += "      " + str(d) + "  "
        for p in range(11, winningPoints+1):
            result +=HitStickOrDouble(QTableDictForQL[p,d,1,0], QTableDictForQL[p,d,1,1], QTableDictForQL[p,d,1,2])

        if (d == 10):
            result +="         10  "
        elif (d == 3):
            result +="      D   3  "
        elif (d == 4):
            result +="      e   4  "
        elif (d == 5):
            result +="      a   5  "
        elif (d == 6):
            result +="      l   6  "
        elif (d == 7):
            result +="      e   7  "
        elif (d == 8):
            result +="      r   8  "
        else:
            result += "      " + str(d) + "  "

        for p in range(11, winningPoints+1):
            result +=HitStickOrDouble(QTableDictForQL[p,d,0,0], QTableDictForQL[p,d,0,1], QTableDictForQL[p,d,0,2])

        result += "<br>"
    result += "<br>"

    for i in range(0, winningPoints*3-17):
        result +=" "
    result +="Sarsa"
    result += "<br>"

    result +="              player (usable ace)"
    for i in range(0, winningPoints*3-36):
        result +=" "
    result +="player (no usable ace)<br>"

    result +="         "
    for p in range(11, winningPoints+1):
        result += str(p)
    result +="             "
    for p in range(11, winningPoints+1):
        result += str(p)
    result += "<br>"

    for d in range (1,11):
        if (d == 10):
            result +="      10   "
        elif (d == 3):
            result +="    D  3   "
        elif (d == 4):
            result +="    e  4   "
        elif (d == 5):
            result +="    a  5   "
        elif (d == 6):
            result +="    l  6   "
        elif (d == 7):
            result +="    e  7   "
        elif (d == 8):
            result +="    r  8   "
        else:
            result += "      " + str(d) + "  "

        for p in range(11, winningPoints+1):
            result +=HitStickOrDouble(QTableDictForSS[p,d,1,0], QTableDictForSS[p,d,1,1], QTableDictForSS[p,d,1,2])

        if (d == 10):
            result +="         10  "
        elif (d == 3):
            result +="      D   3  "
        elif (d == 4):
            result +="      e   4  "
        elif (d == 5):
            result +="      a   5  "
        elif (d == 6):
            result +="      l   6  "
        elif (d == 7):
            result +="      e   7  "
        elif (d == 8):
            result +="      r   8  "
        else:
            result += "      " + str(d) + "  "

        for p in range(11, winningPoints+1):
            result +=HitStickOrDouble(QTableDictForSS[p,d,0,0], QTableDictForSS[p,d,0,1], QTableDictForSS[p,d,0,2])

        result += "<br>"
    result += "<br>"

    for i in range(0, winningPoints*3-23):
        result +=" "
    result +="Temporal Difference"
    result += "<br>"

    result +="              player (usable ace)"
    for i in range(0, winningPoints*3-36):
        result +=" "
    result +="player (no usable ace)<br>"

    result +="         "
    for p in range(11, winningPoints+1):
        result += str(p)
    result +="             "
    for p in range(11, winningPoints+1):
        result += str(p)
    result += "<br>"

    for d in range (1,11):
        if (d == 10):
            result +="      10   "
        elif (d == 3):
            result +="    D  3   "
        elif (d == 4):
            result +="    e  4   "
        elif (d == 5):
            result +="    a  5   "
        elif (d == 6):
            result +="    l  6   "
        elif (d == 7):
            result +="    e  7   "
        elif (d == 8):
            result +="    r  8   "
        else:
            result += "      " + str(d) + "  "

        for p in range(11, winningPoints+1):
             result +=HitStickOrDouble(QTableDictForMC[p,d,1,0], QTableDictForMC[p,d,1,1], QTableDictForMC[p,d,1,2])

        if (d == 10):
            result +="         10  "
        elif (d == 3):
            result +="      D   3  "
        elif (d == 4):
            result +="      e   4  "
        elif (d == 5):
            result +="      a   5  "
        elif (d == 6):
            result +="      l   6  "
        elif (d == 7):
            result +="      e   7  "
        elif (d == 8):
            result +="      r   8  "
        else:
            result += "      " + str(d) + "  "

        for p in range(11, winningPoints+1):
            result +=HitStickOrDouble(QTableDictForMC[p,d,0,0], QTableDictForMC[p,d,0,1], QTableDictForMC[p,d,0,2])

        result += "<br>"

    return render_template('result.html', result=result)




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)



    


 
