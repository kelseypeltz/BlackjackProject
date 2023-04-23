import random
import itertools
import numpy as np
import streamlit as st

# Define the values of the cards
card_values = {
    'Ace': 11,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10
}

# Define the suits of the cards
card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Define the default rules for the game
num_decks = 1
initial_dealt_cards = 2
winning_points = 21
dealer_hit_strategy = 18
double_down_options = 1

# Check if the user wants to use custom rules
if st.session_state.typical_settings == 'no':
    initial_dealt_cards = st.session_state.initial_dealt_cards
    winning_points = st.session_state.winning_points
num_decks = st.session_state.num_decks
dealer_hit_strategy = st.session_state.hit_or_stand
double_down_options = st.session_state.double_cards

# Define a function to create a deck of cards
def create_deck():
    deck = list(itertools.product(card_values.keys(), card_suits))
    random.shuffle(deck)
    return deck

# Define a function to calculate the value of a hand
def calculate_hand_value(hand):
    # Create a list of the values of each card in the hand
    card_values_list = [card_values[card[0]] for card in hand]
    # Check if the hand contains an Ace that should be counted as 1
    if sum(card_values_list) > winning_points and 'Ace' in [card[0] for card in hand]:
        return sum(card_values_list) - 10
    return sum(card_values_list)

# Define a function to play a round of blackjack
def play_blackjack():
    # Create the deck(s) of cards
    deck = create_deck() * num_decks

    # Deal the initial hands
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Check for player blackjack
    if calculate_hand_value(player_hand) == winning_points:
        return 'Player blackjack!', player_hand, dealer_hand

    # Player's turn
    while calculate_hand_value(player_hand) < winning_points:
        # Check if the player wants to double down
        if len(player_hand) == 2 and double_down_options in [1, 2] and sum(card_values[card[0]] for card in player_hand) in [9, 10, 11]:
            if double_down_options == 1 or (double_down_options == 2 and sum(card_values[card[0]] for card in player_hand) != 9):
                if st.button('Double down'):
                    player_hand.append(deck.pop())
                    break

        # Ask the player to hit or stand
        if st.button('Hit'):
            player_hand.append(deck.pop())
        else:
            break

    # Check if the player busted
    if calculate_hand_value(player_hand) > winning_points:
        return 'Player busts!', player_hand, dealer_hand

    # Dealer's turn
    while calculate_hand_value(dealer_hand) < dealer_hit_strategy:
        dealer_hand.append(deck.pop())

    #
    # Check if the dealer busted
    if calculate_hand_value(dealer_hand) > winning_points:
        return 'Dealer busts!', player_hand, dealer_hand

    # Compare the hands
    if calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand):
        return 'Player wins!', player_hand, dealer_hand
    elif calculate_hand_value(player_hand) < calculate_hand_value(dealer_hand):
        return 'Dealer wins!', player_hand, dealer_hand
    else:
        return 'Push!', player_hand, dealer_hand


# Set up the Streamlit app
st.title('Blackjack Game')

st.write('Configure the settings for your blackjack game below. Hit play when you\'re ready to play.')

# Create the form for the user to input the game settings
typical_settings = st.selectbox('Do you want to use typical amount of initial dealt cards (2 cards per player) and blackjack winning points (sum of 21)?', ['Yes', 'No'])

if typical_settings == 'No':
    initial_dealt_cards = st.number_input('Enter the number of initial dealt cards:', min_value=1, value=2)
    winning_points = st.number_input('Enter the number of winning points for blackjack:', min_value=1, value=21)

num_decks = st.number_input('Enter number of decks:', min_value=1, value=1)

hit_or_stand = st.selectbox('Select the dealer\'s strategy:', ['Dealer hits on soft 17', 'Dealer stands on soft 17'])
if hit_or_stand == 'Dealer hits on soft 17':
    dealer_hit_strategy = 18
else:
    dealer_hit_strategy = 17

double_cards = st.selectbox('What cards are you permitted to double?', ['Any 2 cards', '9, 10 & 11 only', '10 & 11 only'])
if double_cards == 'Any 2 cards':
    double_down_options = 1
elif double_cards == '9, 10 & 11 only':
    double_down_options = 2
else:
    double_down_options = 3

if st.button('Play'):
    result, player_hand, dealer_hand = play_blackjack()
    st.write(result)
    st.write('Player hand:', player_hand)
    st.write('Dealer hand:', dealer_hand)


