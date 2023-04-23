
from flask import Flask, request, render_template, url_for, session
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

app = Flask(__name__)
app.secret_key = 'mysecretkey'


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
    QTableDictForQL6, game_results_htmlQL6, win_rateQL6, win_rate_iterationQL6, resultQL6, QTableDiffListQL6 = bt.TrainAndTestGameBot(50000, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS6, game_results_htmlSS6, win_rateSS6, win_rate_iterationSS6, resultSS6, QTableDiffListSS6  = bt.TrainAndTestGameBot(50000, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC6, game_results_htmlMC6, win_rateMC6, win_rate_iterationMC6, resultMC6, QTableDiffListMC6= bt.TrainAndTestGameBot(50000, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
       # train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
    QTableDictForQL5, game_results_htmlQL5, win_rateQL5, win_rate_iterationQL5, resultQL5, QTableDiffListQL5 = bt.TrainAndTestGameBot(10000, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS5, game_results_htmlSS5, win_rateSS5, win_rate_iterationSS5, resultSS5, QTableDiffListSS5 = bt.TrainAndTestGameBot(10000, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC5, game_results_htmlMC5, win_rateMC5, win_rate_iterationMC5, resultMC5, QTableDiffListMC5 = bt.TrainAndTestGameBot(10000, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
   
    game_results_htmlBS, win_rateBS, win_rate_iterationBS, resultBS = br.TestGameBot(10000, DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)


    # report strategy result
    result = "" 
        
    QL = [resultQL1[0], resultQL2[0], resultQL3[0], resultQL4[0], resultQL5[0], resultQL6[0]]    
    SS = [resultSS1[0], resultSS2[0], resultSS3[0], resultSS4[0], resultSS5[0], resultSS6[0]]    
    MC = [resultMC1[0], resultMC2[0], resultMC3[0], resultMC4[0], resultMC5[0], resultMC6[0]]  
    BS = [resultBS[0]]  
        # set width of bar
    barWidth = 0.25
    fig, ax = plt.subplots(figsize =(12, 8))
    # Set position of bar on X axis
    br1 = np.arange(len(QL))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    
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
            ['1', '10', '100', '1000', '10000', '50000'])
            
        
     
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
 #got to do this, maybe have Jake work on it 
    
def create_deck(num_decks):
    """Create and return a shuffled deck of cards with the given number of decks."""
    ranks = list(range(2, 11)) + ['J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    cards = [(rank, suit) for rank in ranks for suit in suits for i in range(num_decks)]
    random.shuffle(cards)
    return cards

    # multiply the cards by the number of decks, then shuffle the deck
    deck = cards * num_decks
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
    QTableDictForQL, game_results_htmlQL, win_rateQL, win_rate_iterationQL, resultQL, QTableDiffListQL = bt.TrainAndTestGameBot(75000, 10000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForSS, game_results_htmlSS, win_rateSS, win_rate_iterationSS, resultSS, QTableDiffListSS = bt.TrainAndTestGameBot(75000, 10000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    QTableDictForMC, game_results_htmlMC, win_rateMC, win_rate_iterationMC, resultMC, QTableDiffListMC = bt.TrainAndTestGameBot(75000, 10000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    
    game_results_htmlBS, win_rateBS, win_rate_iterationBS, resultBS = br.TestGameBot(10000, DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)





    pairsQTableDictForQL, pairsgame_results_htmlQL = pbt.TrainAndTestGameBot(1, 1, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    pairsQTableDictForSS, pairsgame_results_htmlSS = pbt.TrainAndTestGameBot(1, 1, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
    pairsQTableDictForMC, pairsgame_results_htmlMC = pbt.TrainAndTestGameBot(1, 1, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)

    # lambda function for determine hit, stick, or double
    HitStickOrDouble = lambda hitQ, stickQ, doubleQ: "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"
    # lambda function for determine split, hit, stick, or double for when there is pairs    
    SplitHitStickOrDouble = lambda splitQ, hitQ, stickQ, doubleQ: "P" if splitQ >= hitQ and splitQ >= stickQ and splitQ >= doubleQ else "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"


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
    result += "<table style='border-collapse: collapse;'>"
    
    # create header row
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
        
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForQL[p,d,1,0], QTableDictForQL[p,d,1,1], QTableDictForQL[p,d,1,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
        
    # create label row for player (no usable ace)
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForQL[p,d,0,0], QTableDictForQL[p,d,0,1], QTableDictForQL[p,d,0,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
    
    # close table
    result += "</table>"

        # add header and statistics for Sarsa
    result += game_results_htmlSS

    # create Sarsa strategy chart
    result += "<table style='border-collapse: collapse;'>"
    
    # create header row
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
        
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForSS[p,d,1,0], QTableDictForSS[p,d,1,1], QTableDictForSS[p,d,1,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
        
    # create label row for player (no usable ace)
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForSS[p,d,0,0], QTableDictForSS[p,d,0,1], QTableDictForSS[p,d,0,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
    
    # close table
    result += "</table>"


    
    # add header and statistics for Temporal Difference
    result += game_results_htmlMC
    
    # create Temporal Difference strategy chart
    result += "<table style='border-collapse: collapse;'>"
    
    # create header row
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
        
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForMC[p,d,1,0], QTableDictForMC[p,d,1,1], QTableDictForMC[p,d,1,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
        
    # create label row for player (no usable ace)
    result += "<tr><td rowspan='12' style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>D<br>e<br>a<br>l<br>e<br>r<br>'<br>s<br><br>U<br>p<br>c<br>a<br>r<br>d</td><td colspan='13' style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>player (usable ace)</td></tr>"
    result += "<tr><td></td>"
    for p in range(11, winningPoints+1):
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #FF8C8C;'>{}</td>".format(p)
    result += "</tr>"
    # create rows for each dealer card
    for d in range(1, 11):
        # create row for dealer card
        result += "<tr>"
        # label dealer card
        result += "<td style='border: 1px solid black; padding: 5px; background-color: #b8ccb8;'>{}</td>".format(d if d != 1 else "A")
        # create cells for player (no usable ace)
        for p in range(11, winningPoints+1):
            cell_value = HitStickOrDouble(QTableDictForMC[p,d,0,0], QTableDictForMC[p,d,0,1], QTableDictForMC[p,d,0,2])
            color = "#E6FFE6" if cell_value == "H" else "#FFFFCC" if cell_value == "D" else "#FFE6E6"
            result += "<td style='border: 1px solid black; padding: 5px; background-color: {};'>{}</td>".format(color, cell_value)
        # close row
        result += "</tr>"
    
    # close table
    result += "</table>"    


    
    
    
    return render_template('result.html', result=result)






if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)



    


 
