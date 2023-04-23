
from flask import Flask, request, render_template, url_for
import bottraining as bt
import botrunner as br
import pairsbottraining as pbt
import random
import pandas as pd
import seaborn as sns
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io
from io import BytesIO
import base64
import numpy as np
import csv


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/project")
def project(): 
    return render_template('projectdescription.html')   
    
@app.route("/chartmaker")
def chartmaker(): 
    return render_template('chartmaker.html')        
    
@app.route("/charts", methods=["POST"])
def submit_chart():
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


    # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table, one training round
    QTableDictForQL1, game_results_htmlQL1, win_rateQL1, win_rate_iterationQL1, resultQL1, QTableDiffListQL1 = bt.TrainAndTestGameBot(1, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS1, game_results_htmlSS1, win_rateSS1, win_rate_iterationSS1, resultSS1, QTableDiffListSS1 = bt.TrainAndTestGameBot(1, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC1, game_results_htmlMC1, win_rateMC1, win_rate_iterationMC1, resultMC1, QTableDiffListMC1 = bt.TrainAndTestGameBot(1, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    
        # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL2, game_results_htmlQL2, win_rateQL2, win_rate_iterationQL2, resultQL2, QTableDiffListQL2 = bt.TrainAndTestGameBot(10, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS2, game_results_htmlSS2, win_rateSS2, win_rate_iterationSS2, resultSS2, QTableDiffListSS2  = bt.TrainAndTestGameBot(10, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC2, game_results_htmlMC2, win_rateMC2, win_rate_iterationMC2, resultMC2, QTableDiffListMC2 = bt.TrainAndTestGameBot(10, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
       # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL3, game_results_htmlQL3, win_rateQL3, win_rate_iterationQL3, resultQL3, QTableDiffListQL3 = bt.TrainAndTestGameBot(100, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS3, game_results_htmlSS3, win_rateSS3, win_rate_iterationSS3, resultSS3, QTableDiffListSS3  = bt.TrainAndTestGameBot(100, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC3, game_results_htmlMC3, win_rateMC3, win_rate_iterationMC3, resultMC3, QTableDiffListMC3 = bt.TrainAndTestGameBot(100, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
       # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL4, game_results_htmlQL4, win_rateQL4, win_rate_iterationQL4, resultQL4, QTableDiffListQL4 = bt.TrainAndTestGameBot(1000, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS4, game_results_htmlSS4, win_rateSS4, win_rate_iterationSS4, resultSS4, QTableDiffListSS4  = bt.TrainAndTestGameBot(1000, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC4, game_results_htmlMC4, win_rateMC4, win_rate_iterationMC4, resultMC4, QTableDiffListMC4= bt.TrainAndTestGameBot(1000, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
       # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL5, game_results_htmlQL5, win_rateQL5, win_rate_iterationQL5, resultQL5, QTableDiffListQL5 = bt.TrainAndTestGameBot(10000, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS5, game_results_htmlSS5, win_rateSS5, win_rate_iterationSS5, resultSS5, QTableDiffListSS5 = bt.TrainAndTestGameBot(10000, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC5, game_results_htmlMC5, win_rateMC5, win_rate_iterationMC5, resultMC5, QTableDiffListMC5 = bt.TrainAndTestGameBot(10000, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
    game_results_htmlBS, win_rateBS, win_rate_iterationBS, resultBS = br.TestGameBot(10000, DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)


    # report strategy result
    result = "" 
        
    QL = [resultQL1[0], resultQL2[0], resultQL3[0], resultQL4[0], resultQL5[0]]    
    SS = [resultSS1[0], resultSS2[0], resultSS3[0], resultSS4[0], resultSS5[0]]    
    MC = [resultMC1[0], resultMC2[0], resultMC3[0], resultMC4[0], resultMC5[0]]  
    BS = [resultBS[0]]  
        # set width of bar
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8))
    # Set position of bar on X axis
    br1 = np.arange(len(QL))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
        # Make the plot
    plt.bar(br1, QL, color ='r', width = barWidth,
            edgecolor ='grey', label ='QL')
    plt.bar(br2, SS, color ='g', width = barWidth,
            edgecolor ='grey', label ='SS')
    plt.bar(br3, MC, color ='b', width = barWidth,
            edgecolor ='grey', label ='MC')
    plt.axhline(y=BS[0], color='black', linestyle='-', label='BS')
     
    # Adding Xticks
    plt.xlabel('Trained Iterations', fontweight ='bold', fontsize = 15)
    plt.ylabel('House Edge (%)', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(QL))],
            ['1', '10', '100', '1000', '10000'])
            
        
     
    plt.legend()
    
        # Save the plot to a bytes buffer and encode it in base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    bar_houseedge = base64.b64encode(buffer.getvalue()).decode()
    
    # Create the HTML code for the image
    bar_houseedge_html = f'<img src="data:image/png;base64,{bar_houseedge}"/>'
    
        # Add the image HTML code to the result
    result += bar_houseedge_html
    
    # Clear the plot before creating a new one
    plt.clf()
    

    # calculate the change in QTableDict over iterations
    qtable_diffQL = [sum(abs(v) for v in d.values()) for d in QTableDiffListQL5]

    # plot the change in QTableDict
    plt.plot(qtable_diffQL, label='QL')
    
    # calculate the change in QTableDict over iterations
    qtable_diffSS = [sum(abs(v) for v in d.values()) for d in QTableDiffListSS5]
    # plot the change in QTableDict
    plt.plot(qtable_diffSS, label='SS')
    
    # calculate the change in QTableDict over iterations
    qtable_diffMC = [sum(abs(v) for v in d.values()) for d in QTableDiffListMC5]


    # plot the change in QTableDict
    plt.plot(qtable_diffMC, label='MC')
    
    # set the title and axis labels
    plt.title('Change in QTableDict over Training Iterations')
    plt.xlabel('Training Iteration')
    plt.ylabel('Change in QTableDict')
    
    # show the legend and plot
    plt.legend()
    
    # Save the plot to a bytes buffer and encode it in base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    QTableDiffList = base64.b64encode(buffer.getvalue()).decode()
    
    # Create the HTML code for the image
    QTableDiffList_html = f'<img src="data:image/png;base64,{QTableDiffList}"/>'
    
    # Add the image HTML code to the result

    result += QTableDiffList_html


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

    result += game_results_htmlQL1
    

    
        # add header and statistics for Sarsa
    result += game_results_htmlSS1

    
    # add header and statistics for Temporal Difference
    result += game_results_htmlMC1
    


    
    
    
    
    return render_template('charts.html', result=result)
    
    
    
@app.route("/gamerules")
def gamerules(): 
    return render_template('gamerules.html')   
    
@app.route("/game", methods=['GET', 'POST'])
def play_game():
    # Initialize deck and player/dealer hands
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
    defaultDeckContent = create_deck()
    
    deck = []
    for item in defaultDeckContent:
      deck += [item]*number_of_decks
      
    player_hand = []
    dealer_hand = []
    
    # Deal initial cards
    while initialNumberOfCard > 0:
        player_hand.append(draw_card(deck))
        initialNumberOfCard -= 1

    dealer_hand.append(draw_card(deck))
    
    # Player's turn
    while sum(player_hand) < winningPoints:
        if request.method == 'POST' and 'hit' in request.form:
            player_hand.append(draw_card(deck))
            if sum(player_hand) == winningPoints:
                return render_template('gameresult.html', result='You win!')
            elif sum(player_hand) > winningPoints:
                return render_template('gameresult.html', result='You bust!')
            else:
                return render_template('play.html', player_hand=player_hand, dealer_hand=dealer_hand)
        elif request.method == 'POST' and 'stand' in request.form:
            break
        else:
            return render_template('play.html', player_hand=player_hand, dealer_hand=dealer_hand)
    
    # Dealer's turn
    while sum(dealer_hand) < dealerCriticalPointsToStick:
        dealer_hand.append(draw_card(deck))
    
    # Determine winner
    if sum(dealer_hand) > winningPoints:
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


    filename = "q_learning_results.csv"

    # create a list to store the results from each iteration
    results = []
        
        # report strategy result
    result = "" 


    for i in range(1, 750002, 1000):
        _, game_results_htmlQL, _, _, resultQL, _ = bt.TrainAndTestGameBot(i, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
        results.append(resultQL)
        QTableDictForSS, game_results_htmlSS, win_rateSS, win_rate_iterationSS, resultSS, QTableDiffListSS = bt.TrainAndTestGameBot(i, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
        results.append(resultSS)
        QTableDictForMC, game_results_htmlMC, win_rateMC, win_rate_iterationMC, resultMC, QTableDiffListMC = bt.TrainAndTestGameBot(i, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
        results.append(resultMC)
    
    return render_template('result.html', result=result)

     




if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)



    


 
