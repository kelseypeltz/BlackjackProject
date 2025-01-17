﻿from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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
                return render_template('result.html', result='You win!')
            elif sum(player_hand) > 21:
                return render_template('result.html', result='You bust!')
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
        return render_template('result.html', result='You win!')
    elif sum(dealer_hand) == sum(player_hand):
        return render_template('result.html', result='Push!')
    elif sum(dealer_hand) > sum(player_hand):
        return render_template('result.html', result='Dealer wins!')
    else:
        return render_template('result.html', result='You win!')
    
def create_deck():
    """Create a new deck of cards."""
    deck = []
    for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
        for rank in range(2, 11):
            deck.append(rank)
        for rank in ['J', 'Q', 'K', 'A']:
            deck.append(rank)
    random.shuffle(deck)
    return deck
    
def draw_card(deck):
    """Remove and return a card from the deck."""
    return deck.pop()

if __name__ == '__main__':
    app.run(debug=True)
