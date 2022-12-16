# BlackjackProject

#test

## Background
This project aims to explore how blackjack rule variation affects the house's edge when a player is using basic strategy. The house edge is the percentage a casino will win over the player. In other words, the house edge is the ratio of the players' average loss to their initial bets. In 1962 Edward Thorp created a basic strategy for blackjack that produces an almost even game (house edge of 0.55%) when played with general casino rules. In a game with general casino rules, it is assumed that the house uses 6 decks and the following rules: double on any first 2 cards, no double after splitting, resplit all pairs except Aces, dealer stands of soft 17, and no surrender. The problem we found was when the rules vary from the general casino rules, the house edge changes, giving a naive player using basic strategy the false assumption that it is an almost even game. In this project, we attempt to model how rule variations affect the house edge to allow players to estimate their true disadvantage (or advantage) when using basic strategy. 

## The Game
Blackjack is the most popular casino banking game in the world. In blackjack, there is one deck of 52 cards, everyone plays against the dealer, players place bets, and each player is dealt two cards at a time (including the dealer). The players know one of the dealer's cards, while the other remains unknown until the round is done. After everyone is dealt, players can decide if they want to "hit," meaning they'd be dealt more cards (one at a time) to get a sum closest to 21 without "busting" (going over 21). If a player is satisfied with their hand, they do not "hit." The goal is to have a sum greater than the dealers.1 Players and dealers often use card counting as away to become an advantaged player. Card counting is a mathematical strategy used in blackjack that helps determine one’s probable advantage or disadvantage of the next dealt card. 

## Basic Strategy 
Here is a chart of Edward Thorp's basic strategy taken from [Blackjackinfo.com](https://www.blackjackinfo.com/blackjack-basic-strategy-engine/). The strategy tells players when to hit (H), stand (S), split (P), and double (D/DS) according to the the sum or combination of their hand and the dealer's known upcard.
