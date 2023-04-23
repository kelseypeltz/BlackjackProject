from collections import defaultdict
import random

def BasicStrategy(playerCardPoints, dealerFirstCardPoint, playerCardUsableAce):
    """
    Implements the basic strategy for Blackjack.
    """
    if playerCardUsableAce:
        # Soft total
        if playerCardPoints >= 19:
            return 1 # stand
        elif playerCardPoints == 18:
            if dealerFirstCardPoint in [9,10,1]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints == 17:
            if dealerFirstCardPoint in [3,4,5,6]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints == 16:
            if dealerFirstCardPoint in [4,5,6]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints in [13,14,15]:
            if dealerFirstCardPoint in [5,6]:
                return 0 # hit
            else:
                return 1 # stand
        else: # playerCardPoints in [2,3,4,5,6,7,8,9,10,11,12]
            return 0 # hit
    else:
        # Hard total
        if playerCardPoints >= 17:
            return 1 # stand
        elif playerCardPoints <= 8:
            return 0 # hit
        elif playerCardPoints == 9:
            if dealerFirstCardPoint in [3,4,5,6]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints == 10:
            if dealerFirstCardPoint in [10,1]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints == 11:
            return 1 # always double down
        elif playerCardPoints == 12:
            if dealerFirstCardPoint in [4,5,6]:
                return 0 # hit
            else:
                return 1 # stand
        elif playerCardPoints in [13,14,15,16]:
            if dealerFirstCardPoint in [2,3,4,5,6]:
                return 0 # hit
            else:
                return 1 # stand
