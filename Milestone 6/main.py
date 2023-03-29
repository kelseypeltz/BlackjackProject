
from flask import Flask, request, render_template, url_for
import bottraining as bt
import botrunner as br
import pairsbottraining as pbt
import random


app = Flask(__name__)


@app.route("/")
def index():

    return (
        """<html>
                <head>
                    <title>Blackjack Game Settings</title>
                    <style>
                      img {
                        width: 100%;
                        height: auto;
                      }
                    </style>
                  </head>
                  <body>
                    <img src="https://www.scu.edu/media/portals/illuminate/images/Illuminate-philkesten-header-30-1160x386.jpeg" alt="First Image">
                    <h1>Blackjack Game Settings</h1>
                    <i>Capstone Project by Jake Johnson & Kelsey Peltz </i>
                    <p><a href="/game">Play a Simulated Game</a></p>
	                <p><a href="/strategymaker">Make a Strategy Chart based off of Your Rule Variations</a></p>
                    <h2>Abstract</h2>
                    <p>This project aims to use reinforcement learning algorithms to teach a computer agent how to play blackjack with a win rate equal to or greater than that of the average professional player. The learning agent takes in rule variations and creates a strategy that mirrors Edward Thorp’s basic strategy. This program can take rule variations of any specific casino and produce an ideal strategy along with a card counting strategy for betting.</p>
                    <h3>Rule Variation Inputs</h3>
                    <p>Since Thorp's book was published in 1962, his basic strategy has become widespread knowledge, forcing casinos to tweak their rules to gain their edge back. Some of the most common rule changes include:</p>
                    <p>- The dealer hits on soft 17</p>
                    <p>- No double on aces after splitting</p>
                    <p>- Blackjacks payout at 6:5 instead of 3:2</p>
                    <p>- Dealer doesn't peek to see if they have blackjack</p>
                    <p>- Penetration percentage each deal</p>
                    <p>- Automatic shuffler vs Dealer shoe shuffle</p>
                    <h2>Background</h2>
                    <p>This project aims to explore how blackjack rule variation affects the house's edge when a player is using basic strategy. The house edge is the percentage a casino will win over the player. In other words, the house edge is the ratio of the players' average loss to their initial bets. In 1962 Edward Thorp created a basic strategy for blackjack that produces an almost even game (house edge of 0.55%) when played with general casino rules. In a game with general casino rules, it is assumed that the house uses 6 decks with the following rules: double on any first 2 cards, no double after splitting, resplit all pairs except Aces, dealer stands on soft 17, and no surrender. The problem we found was when the rules vary from the general casino rules, the house edge changes, giving a naive player using basic strategy the false assumption that it is an almost even game. In this project, we attempt to model how rule variations affect the house edge to allow players to estimate their true disadvantage (or advantage) when using basic strategy.</p>
                    <h2>The Game</h2>
                    <p>Blackjack is the most popular casino banking game in the world. In blackjack, there is one deck of 52 cards, everyone plays against the dealer, players place bets, and each player is dealt two cards at a time (including the dealer). The players know one of the dealer's cards, while the other remains unknown until the round is done. After everyone is dealt, players can decide if they want to "hit," meaning they'd be dealt more cards (one at a time) to get a sum closest to 21 without "busting" (going over 21). If a player is satisfied with their hand, they do not "hit." The goal is to have a sum greater than the dealers. Professional players may use card counting as a way to become an advantaged player. Card counting is a mathematical strategy used in blackjack that helps determine one’s probable advantage or disadvantage of the next dealt card, which the player can use to decide when to increase their betting amount.</p>
        </body>
    </html>"""
    )
    
@app.route("/game", methods=['GET', 'POST'])
def play_game():
    # Initialize deck and player/dealer hands
    deck = create_deck()
    player_hand = []
    dealer_hand = []
    
    # Deal initial cards
    player_hand.append(draw_card(deck))
    player_hand.append(draw_card(deck))
    dealer_hand.append(draw_card(deck))
    
    # Player's turn
    while sum(player_hand) < 21:
        if request.method == 'POST' and 'hit' in request.form:
            player_hand.append(draw_card(deck))
            if sum(player_hand) == 21:
                return render_template('gameresult.html', result='You win!')
            elif sum(player_hand) > 21:
                return render_template('gameresult.html', result='You bust!')
            else:
                return render_template('play.html', player_hand=player_hand, dealer_hand=dealer_hand)
        elif request.method == 'POST' and 'stand' in request.form:
            break
        else:
            return render_template('play.html', player_hand=player_hand, dealer_hand=dealer_hand)
    
    # Dealer's turn
    while sum(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))
    
    # Determine winner
    if sum(dealer_hand) > 21:
        return render_template('gameresult.html', result='You win!')
    elif sum(dealer_hand) == sum(player_hand):
        return render_template('gameresult.html', result='Push!')
    elif sum(dealer_hand) > sum(player_hand):
        return render_template('gameresult.html', result='Dealer wins!')
    else:
        return render_template('gameresult.html', result='You win!')
    
def create_deck():
    """Create a new deck of cards."""
    deck = []
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        for rank in range(2, 11):
            deck.append(str(rank))
        for rank in ['J', 'Q', 'K', 'A']:
            deck.append(rank)
    random.shuffle(deck)
    return deck
    
def draw_card(deck):
    """Remove and return a card from the deck."""
    card = deck.pop()
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11
    else:
        return int(card)
    
@app.route("/strategymaker")
def strategymaker(): 
    return render_template('strategymaker.html')    
    

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
    QTableDictForQL, game_results_htmlQL = bt.TrainAndTestGameBot(100000, 100000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS, game_results_htmlSS = bt.TrainAndTestGameBot(100000, 100000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC, game_results_htmlMC = bt.TrainAndTestGameBot(100000, 100000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    
    pairsQTableDictForQL, pairsgame_results_htmlQL = pbt.TrainAndTestGameBot(100000, 100000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    pairsQTableDictForSS, pairsgame_results_htmlSS = pbt.TrainAndTestGameBot(100000, 100000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    pairsQTableDictForMC, pairsgame_results_htmlMC = pbt.TrainAndTestGameBot(100000, 100000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)

    # lambda function for determine hit, stick, or double
    HitStickOrDouble = lambda hitQ, stickQ, doubleQ: "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"
    # lambda function for determine split, hit, stick, or double for when there is pairs    
    SplitHitStickOrDouble = lambda splitQ, hitQ, stickQ, doubleQ: "P" if splitQ >= hitQ and splitQ >= stickQ and splitQ >= doubleQ else "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"


    game_results_htmlBS = br.TestGameBot(100000, DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)

    # report strategy result
    result = "" 
    result += f"""
    <html>
        <head>
            <title>Blackjack Game Results</title>
        </head>
        <body>           
            <h2>User's set Rules:</h2>
            <p>Number of decks: {number_of_decks}</p>
            <p>Initial number of cards: {initialNumberOfCard}</p>
            <p>Winning points: {winningPoints}</p>
            <p>{('Dealer hits on soft 17' if dealerCriticalPointsToStick == 18 else 'Dealer stands on soft 17')}</p>
            <p>Double on {(('Any 2 cards' if doubleVariation == 1 else '9, 10 & 11 only') if doubleVariation == 2 else '10 & 11 only')}</p>
        </body>
    </html>
    """
    #report basic strategy and rule variation data
    result += game_results_htmlBS
    
    # add header and statistics for Q-learning

    result += game_results_htmlQL




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
    # create pairs strategy chart for Q-learning
    result += "<table>"
    # create header row
    result += "<tr><td rowspan='12'>Dealer's Upcard</td><td colspan='12'>Player's Pair</td></tr>"
    # create top row of player pairs
    result += "<tr>"
    for p in range(2,20):
        result += "<td>{}</td>".format(p)
    result += "</tr>"
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += f"<td>{d if d != 1 else 'A'}</td>"
        # create cells for player pairs
        for p in range(2, 20):
                cell_value = SplitHitStickOrDouble(pairsQTableDictForQL[p, d, 1, 0], pairsQTableDictForQL[p, d, 1, 1], pairsQTableDictForQL[p, d, 1, 2], pairsQTableDictForQL[p, d, 1, 3])
                result += "<td>{}</td>".format(cell_value)
            # close row
        result += "</tr>"    
    # close table
    result += "</table>"

    
        # add header and statistics for Sarsa
    result += game_results_htmlSS

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
    result += game_results_htmlMC
    
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



    


 
