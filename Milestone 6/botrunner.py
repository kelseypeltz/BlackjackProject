from gameplay import GamePlay
from setstartegy import BasicStrategy
from collections import defaultdict
import sys

class Strategy:
    def __init__(self, playerCardPoints, dealerFirstCardPoint, playerCardUsableAce):
        self.playerCardPoints = playerCardPoints
        self.dealerFirstCardPoint = dealerFirstCardPoint
        self.playerCardUsableAce = playerCardUsableAce

    def BasicStrategyAction(self, playerCardPoints, dealerFirstCardPoint, playerCardUsableAce):
        return BasicStrategy(playerCardPoints, dealerFirstCardPoint, playerCardUsableAce)

def TestGameBot(testingIteration, deckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation):

    #check input parameter robustness
    #check input parameter robustness
    if (initialNumberOfCard * 10 > winningPoints):
        print("This rule combination will not work because initial card points can exceed the winning points, not allowed")
        sys.exit();

    if (initialNumberOfCard < 1):
        print("This rule combination will not work because initial number of card must be equal or greater than one")
        sys.exit();

    if (dealerCriticalPointsToStick > winningPoints):
        print("This rule combination will not work because dealer will hit until bust")
        sys.exit();


    # when player combats with dealer after the training phase,
    # this list stores the result [#win, #draw, #lose]
    testResult = [0, 0, 0];
    


    # Iterate over number of games to test
    for i in range(testingIteration):
        
       # if player wins dealer, reward = 1
        # if player draws dealer, reward = 0
        # if player loses dealer, reward = -1
        # used to update the Q function
        reward = None
        
        # Initialize game
        gameplay = GamePlay(deckContent, initialNumberOfCard, winningPoints, doubleVariation)
        
        # Initialize strategy
        strategy = Strategy(gameplay.playerCardPoints, gameplay.dealerFirstCardPoint, gameplay.playerCardUsableAce)
        
        # Play game until finished
        while not gameplay.finish:
            
            # Determine action using BasicStrategy
            action = BasicStrategy(gameplay.playerCardPoints, gameplay.dealerFirstCardPoint, gameplay.playerCardUsableAce)

            
            # Proceed with the action
            gameplay.playerCardPoints, gameplay.dealerCardPoints, gameplay.playerCardUsableAce, reward = gameplay.GameProceed(gameplay, action, winningPoints, dealerCriticalPointsToStick, doubleVariation)
            
                        # game is finished if reward is out
            if (reward is not None):
                gameplay.finish = True
    #  # update test result
        if (reward == 1):
            testResult [0] += 1
        elif (reward == -1):
            testResult [2] += 1
        else:
            testResult [1] += 1



    print("Our game bot fights against the dealer for ", testingIteration, " rounds using Basic Strategy")
    print("Win: ", (float)(testResult [0])/testingIteration*100.0, "%")
    print("Draw: ", (float)(testResult [1])/testingIteration*100.0, "%")
    print("Lose: ", (float)(testResult [2])/testingIteration*100.0, "%")
    print()
    
    game_results_html =  f"""
    <html>
        <head>
            <title>Blackjack Game Results</title>
        </head>
        <body>
            <h2>Blackjack Game Results if you had used Basic Strategy</h2>
            <b><i>House edge: {(float)(testResult[2])/testingIteration*100.0 + (float)(testResult[0])/testingIteration*(-100.0)}%<b><i>
            <p>Win: {(float)(testResult[0]) / testingIteration * 100}%</p>
            <p>Draw: {(float)(testResult[1]) / testingIteration * 100}%</p>
            <p>Lose: {(float)(testResult[2]) / testingIteration * 100}%</p>
        </body>
    </html>
    """
    return game_results_html
    
    
    


