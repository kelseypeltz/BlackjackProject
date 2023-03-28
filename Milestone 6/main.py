from flask import Flask
from flask import request
from flask import render_template

import bottraining as bt


app = Flask(__name__)


@app.route("/")
def index():
    title = "Blackjack Game Settings"
    description = "This is Jake and Kelsey's capstone project. Configure the settings for your blackjack game below."

    return (
        """<html>
                <head>
                    <title>Blackjack Game Settings</title>
                    <style>
                        img {
                            width: 50%;
                            height: auto;
                        }
                    </style>
                </head>
                <body>
                    <img src="images/first_image.jpg" alt="First Image">
                    <h1>Blackjack Game Settings</h1>
                    <p>This is Jake and Kelsey's capstone project. Configure the settings for your blackjack game below.</p>
                    <form method="POST" action="/submit">
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
            </script>
        </body>
    </html>"""
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
    
    # add header and statistics for Q-learning
    result += "<h3>Q-learning</h3>"
    
# create Q-learning strategy chart
    result += "<table>"

    # create header row
    result += "<tr><td rowspan='12'>Dealer's Upcard</td><td colspan='12'>player (usable ace)</td><td></td><td colspan='12'>player (no usable ace)</td></tr>"

# create top row of player cards

    # create top row of player cards
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "<td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "</tr>"
    
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForQL[p,d,1,0], QTableDictForQL[p,d,1,1], QTableDictForQL[p,d,1,2])
            result += "<td>{}</td>".format(cell_value)
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForQL[p,d,0,0], QTableDictForQL[p,d,0,1], QTableDictForQL[p,d,0,2])
            result += "<td>{}</td>".format(cell_value)
        # close row
        result += "</tr>"    
    # close table
    result += "</table>"    
    
        # add header and statistics for Sarsa
    result += "<h3>Sarsa</h3>"

    # create Sarsa strategy chart
    result += "<table>"

    # create header row
    result += "<tr><td rowspan='12'>Dealer's Upcard</td><td colspan='12'>player (usable ace)</td><td></td><td colspan='12'>player (no usable ace)</td></tr>"


    # create top row of player cards
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "<td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "</tr>"
    
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForSS[p,d,1,0], QTableDictForSS[p,d,1,1], QTableDictForSS[p,d,1,2])
            result += "<td>{}</td>".format(cell_value)
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForSS[p,d,0,0], QTableDictForSS[p,d,0,1], QTableDictForSS[p,d,0,2])
            result += "<td>{}</td>".format(cell_value)
        # close row

        result += "</tr>"    
    # close table
    result += "</table>"    
    
    # add header and statistics for Temporal Difference
    result += "<h3>Temporal Difference</h3>"
    
    # create Temporal Difference strategy chart
    result += "<table>"    
    # create header row
    result += "<tr><td rowspan='12'>Dealer's Upcard</td><td colspan='12'>player (usable ace)</td><td></td><td colspan='12'>player (no usable ace)</td></tr>"

# create top row of player cards

    # create top row of player cards
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "<td></td>"
    for p in range(11, winningPoints+1):
        result += "<td>{}</td>".format(p)
    result += "</tr>"
    
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForMC[p,d,1,0], QTableDictForMC[p,d,1,1], QTableDictForMC[p,d,1,2])
            result += "<td>{}</td>".format(cell_value)
        # label dealer card
        result += "<td>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForMC[p,d,0,0], QTableDictForMC[p,d,0,1], QTableDictForMC[p,d,0,2])
            result += "<td>{}</td>".format(cell_value)
        # close row
        result += "</tr>"    
    # close table
    result += "</table>"    
    
    
    
    
    return render_template('result.html', result=result)






if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)



    


 
