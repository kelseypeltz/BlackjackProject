
> ![image](https://user-images.githubusercontent.com/69976409/195754514-06dcba6c-7ea4-42da-a3d8-8f334194c1f8.png)
# Blackjack Project
Approach to Blackjack by Jake Johnston & Kelsey Peltz
### [Website Link](https://jakeriverj.github.io/BlackjackProject/)
<details open="open">
<summary>Table of Contents</summary>
- [The Game](#the-game)
- [Project Goals](#project-goals)
  - [Collaboration Plan](#collaboration-plan)
- [ETL](#etl)
   
   
</details>

---   
## Background
This project aims to explore how blackjack rule variation affects the house's edge when a player is using basic strategy. The house edge is the percentage a casino will win over the player. In other words, the house edge is the ratio of the players' average loss to their initial bets. In 1962 Edward Thorp created a basic strategy for blackjack that produces an almost even game (house edge of 0.55%) when played with general casino rules. In a game with general casino rules, it is assumed that the house uses 6 decks with the following rules: double on any first 2 cards, no double after splitting, resplit all pairs except Aces, dealer stands on soft 17, and no surrender. The problem we found was when the rules vary from the general casino rules, the house edge changes, giving a naive player using basic strategy the false assumption that it is an almost even game. In this project, we attempt to model how rule variations affect the house edge to allow players to estimate their true disadvantage (or advantage) when using basic strategy. 

## The Game
Blackjack is the most popular casino banking game in the world. In blackjack, there is one deck of 52 cards, everyone plays against the dealer, players place bets, and each player is dealt two cards at a time (including the dealer). The players know one of the dealer's cards, while the other remains unknown until the round is done. After everyone is dealt, players can decide if they want to "hit," meaning they'd be dealt more cards (one at a time) to get a sum closest to 21 without "busting" (going over 21). If a player is satisfied with their hand, they do not "hit." The goal is to have a sum greater than the dealers. Professional players may use card counting as a way to become an advantaged player. Card counting is a mathematical strategy used in blackjack that helps determine one’s probable advantage or disadvantage of the next dealt card, which the player can use to decide when to increase their betting amount. 

## Basic Strategy 
Here is a chart of Edward Thorp's basic strategy taken from [chasingthefrog.com](http://www.chasingthefrog.com/reelfaces/21basicstrategy.php). The strategy tells players when to hit (H), stand (S), split (P), and double (D/DS) according to the the sum or combination of their hand and the dealer's known upcard.

<img width="319" alt="Screen Shot 2022-12-15 at 8 00 29 PM" src="https://user-images.githubusercontent.com/77644658/208005154-d0f4bae4-b9a4-4811-ac3e-8783410347a2.png">


## Rule Variations
Since Thorp's book was published in 1962, his basic strategy has become widespread knowledge, forcing casinos to tweak their rules to gain their edge back. Some of the most common rule changes include:
  - The dealer hits on soft 17
  - No double on aces after splitting
  - Blackjacks payout at 6:5 instead of 3:2
  - Dealer doesn't peek to see if they have blackjack
  - Penetration percentage each deal
  - Automatic shuffler vs Dealer shoe shuffle

## ETL 
### (Extract, Transform, and Load)
Currently we are coding a blackjack simulation that will run the game thousands of times using different strategies since the data source we had been hoping to use was too large for github. We are hoping to somehow upload the data from [here](https://www.kaggle.com/datasets/mojocolors/900000-hands-of-blackjack-results) to get more insights into the average player. In the meantime, we found a smaller dataset to begin analyzing. We also compiled to help us understand blackjack basic strategy (a.k.a. the book) and the "typical" human strategy so we can compare those with the counting card strategies. 

### Wizard of Vegas Casino Survey

![logo](https://user-images.githubusercontent.com/77644658/208007591-446b96e7-038b-4d80-b3a4-999ae8a9e418.png)

Our research on various rule changes led us to a website curated by Michael Shackleford, a professor of actuarial science and mathematics at the University of Nevada, Las Vegas. On his site, [Wizard Of Vegas](https://wizardofvegas.com/guides/blackjack-survey/) he posts reports taken from the monthly Current Blackjack News survey. By scraping the Wizard of Odds and Wizard of Vegas websites, we were able to get a database with every Las Vegas casino and their respective rules for their blackjack tables:

```
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
```

```
r = requests.get('https://wizardofvegas.com/guides/blackjack-survey/')
soup = BeautifulSoup( r.content )
soup.find("table")
list_vegascasinos = pd.read_html(str(soup.find("table")))
df_casinodata = list_vegascasinos[0]
df_casinodata[0:10]
```
<img width="1021" alt="Screen Shot 2022-12-15 at 7 38 09 PM" src="https://user-images.githubusercontent.com/77644658/208002196-54c70340-cc74-4602-b12c-db80065e2600.png">

After cleaning up and reordering the dataframe, we had columns for the calculated house edge, number of decks, cut (penetration perentage), and rules for each Las Vegas casino.


## Collaboration Plan 

We have set up a google colab to work on our code together. Since we are partnering this project with our Capstone project, we plan on meeting on a weekly to bi-weekly schedule our faculty mentor. We plan on dividing work by doing independent research and coding and discussing it during our scheduled meetings and throughout the week as needed. 


