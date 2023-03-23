import bottraining as bt


  # cards for one deck game
defaultDeckContent = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                      '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                      '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                      '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']

number_of_decks = int(input("Enter number of decks:"))

DeckContent = []
for item in defaultDeckContent:
  DeckContent += [item]*number_of_decks

# Ask the user if they want to use typical settings
use_typical_settings = input("Do you want to use typical amount of initial dealt cards (2 cards per player) and blackjack winning points (sum of 21)? (yes/no) ")

if use_typical_settings.lower() == "yes":
    # Use typical settings
    initialNumberOfCard = 2
    winningPoints = 21
else:
    # Ask for user input for custom settings
    initialNumberOfCard = int(input("Enter the number of initial dealt cards: "))
    winningPoints = int(input("Enter the number of winning points for blackjack: "))

# Ask the user if the dealer hits or stand on soft 17 

hit_or_stand = int(input("Enter 1 for dealer hits on soft 17. Enter 2 for dealer stands on soft 17:"))
# Dealer hits on soft 17
if hit_or_stand == 1:
  dealerCriticalPointsToStick = 18

# Dealer stands on soft 17  
if hit_or_stand == 2:
  dealerCriticalPointsToStick = 17

# Ask the user about which doubleVariation they are following 
any_two = input("Are you permitted to double any 2 cards? (yes/no) ")

if any_two.lower() == "yes":
  doubleVariation = 1 

else:
  double_three = input("Are you permitted to double 9, 10 & 11? (yes/no ")  

  if double_three.lower() == "yes":
    doubleVariation = 2

  else:
    print("You are permitted to double 10 & 11 only")
    doubleVariation = 3

             
# train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table
QTableDictForQL = bt.TrainAndTestGameBot(100000, 100000, "Q-Learning", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
QTableDictForSS = bt.TrainAndTestGameBot(100000, 100000, "Sarsa", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)
QTableDictForMC = bt.TrainAndTestGameBot(100000, 100000, "Temporal Difference", DeckContent, initialNumberOfCard, winningPoints, dealerCriticalPointsToStick, doubleVariation)

# lambda function for determine hit, stick, or double
HitStickOrDouble = lambda hitQ, stickQ, doubleQ: "D" if doubleQ >= hitQ and doubleQ >= stickQ else "H" if hitQ >= stickQ else "S"


# report strategy result
for i in range(0, winningPoints*3-17):
    print(" ", end = "")
print("Q-learning", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winningPoints*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("         ", end = " ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print("             ", end=" ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")
    for p in range(11, winningPoints+1):
        print(HitStickOrDouble(QTableDictForQL[p,d,1,0], QTableDictForQL[p,d,1,1], QTableDictForQL[p,d,1,2]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winningPoints+1):
        print(HitStickOrDouble(QTableDictForQL[p,d,0,0], QTableDictForQL[p,d,0,1], QTableDictForQL[p,d,0,2]), "", end = " ")

    print()
print()

for i in range(0, winningPoints*3-17):
    print(" ", end = "")
print("Sarsa", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winningPoints*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("         ", end = " ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print("             ", end=" ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")

    for p in range(11, winningPoints+1):
        print(HitStickOrDouble(QTableDictForSS[p,d,1,0], QTableDictForSS[p,d,1,1], QTableDictForSS[p,d,1,2]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winningPoints+1):
        print(HitStickOrDouble(QTableDictForSS[p,d,0,0], QTableDictForSS[p,d,0,1], QTableDictForSS[p,d,0,2]), "", end = " ")

    print()
print()

for i in range(0, winningPoints*3-23):
    print(" ", end = "")
print("Temporal Difference", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winningPoints*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("         ", end = " ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print("             ", end=" ")
for p in range(11, winningPoints+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")

    for p in range(11, winningPoints+1):
         print(HitStickOrDouble(QTableDictForMC[p,d,1,0], QTableDictForMC[p,d,1,1], QTableDictForMC[p,d,1,2]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winningPoints+1):
        print(HitStickOrDouble(QTableDictForMC[p,d,0,0], QTableDictForMC[p,d,0,1], QTableDictForMC[p,d,0,2]), "", end = " ")

    print()

