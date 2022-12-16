
> ![image](https://user-images.githubusercontent.com/69976409/195754514-06dcba6c-7ea4-42da-a3d8-8f334194c1f8.png)
# Blackjack Rule Variations and How They Affect the Casino's Edge
### by Jake Johnston & Kelsey Peltz
### Final Data Science Tutorial - CMPS 3660 - Introduction to Data Science - Professor Mattei
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

#### Wizard of Vegas

![logo](https://user-images.githubusercontent.com/77644658/208007591-446b96e7-038b-4d80-b3a4-999ae8a9e418.png)

Our research on various rule changes led us to a website curated by Michael Shackleford, a professor of actuarial science and mathematics at the University of Nevada, Las Vegas. On his site, [Wizard Of Vegas](https://wizardofvegas.com/guides/blackjack-survey/), he posts reports taken from the monthly Current Blackjack News survey. By scraping the Wizard of Odds and Wizard of Vegas websites, we were able to extract data on every Las Vegas casino and their respective rules for their blackjack tables:

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
casinodata_df = list_vegascasinos[0]
casinodata_df[0:10]
```
<img width="950" alt="Screen Shot 2022-12-15 at 9 14 45 PM" src="https://user-images.githubusercontent.com/77644658/208013813-1decff55-fe3c-42b5-a58c-bef9f6e04533.png">

After scraping the casino data, we saved it as a csv and read it into a new, temporary DataFrame object called temp. From temp, we removed missing values that were created as a result of formatting issues from scrapping and called this dataframe casino_data. To make the rules easier to analyze, we converted them into strings.
```
temp = pd.read_csv("/content/drive/MyDrive/Blackjack Data Science Project/CasinoTable.csv")
casino_data = temp.dropna(axis=0)
casino_data['Rules'] = casino_data.Rules.apply(lambda x: x[0:].split(','))
casino_data.head()
```
![casino_data](https://github.com/kelseypeltz/blackjackproject.github.io/blob/9190d82ba605c8f0ab081acd39b10959fd82420c/Screen%20Shot%202022-12-15%20at%2010.02.54%20PM.png)

On the same site, we also found a list of every possible blackjack rule variation along with the percent increase or decrease that it has on the player's edge:
```
r2 = requests.get('https://wizardofodds.com/games/blackjack/rule-variations/')
soup_rules = BeautifulSoup( r2.content )
soup_rules.find("table")
list_rules = pd.read_html(str(soup_rules.find("table")))
rules_df = list_rules[0]
rules_df[0:10]
```
<img width="349" alt="Screen Shot 2022-12-15 at 9 12 57 PM" src="https://user-images.githubusercontent.com/77644658/208013719-90782f8e-5099-43db-9cd6-baecf8ef64e7.png">

We then converted each rule to their respective letter code (h17 = Dealer hits soft 17, s17 = Dealer stands soft 17, ds = Double after splitting, ls = Late surrender, etc.) so that the rules_df could be used in parallel with the casino_df. After cleaning up and reordering the casino_df, we had columns for:
  - number of tables
  - calculated house edge
  - number of decks
  - cut (penetration perentage)
  - minimum bet
  - maximum bet
  - rules

## Exploratory Data Analysis

We started our exploratory data analysis by finding the default casino edge for each deck size assuming that the game was played under traditional rules. We then found the means of the casinos' edges grouped by the number of decks they used.
```
(casino_data[casino_data.Decks == 1.0]['Edge'].mean(), casino_data[casino_data.Decks == 2.0]['Edge'].mean(), casino_data[casino_data.Decks == 6.0]['Edge'].mean(), casino_data[casino_data.Decks == 8.0]['Edge'].mean())

```
Which gave us the following results:
- 1 deck: 0.18
- 2 decks: 0.38899999999999996
- 6 decks: 0.4338235294117647
- 8 decks: 0.5427272727272728

We wanted to see how the combination of penetration of a deck and number of decks affected the mean of the edge. We found that the mean of the houses' edge was largest when there were six decks combined with a 1.4 deck cut. 8 decks overall resulted in largest mean of the houses' edge. The smallest mean by far was when the house used 1 deck. Using only 1 deck is very rare which resulted in us only having one data point so the mean of 1 deck houses' edges might not be a good representation. 

```
edge_decks_cut_mean = casino_data.groupby(["Decks",'Cut'])["Edge"].mean()
edge_decks_cut_mean.to_frame()
edge_decks_cut_mean.plot.bar()
```
![edge.deck.cut table](https://github.com/kelseypeltz/blackjackproject.github.io/blob/156a24348dde0c6e41225801953aa9f6d1720629/Screen%20Shot%202022-12-15%20at%2010.12.40%20PM.png)
![edge.deck.cut graph](https://github.com/kelseypeltz/blackjackproject.github.io/blob/156a24348dde0c6e41225801953aa9f6d1720629/Screen%20Shot%202022-12-15%20at%2010.12.55%20PM.png)

Here we showed a visual representation of our calculated default edge with the actual houses' edges means. As you can see, our calculated default edge is very close the actual houses' mean for 2 decks and 8 decks. For 1 and 6 decks, our calculated default varies from the actual mean which was expected due to rule variation. 

![estimate vs actual mean](https://github.com/kelseypeltz/blackjackproject.github.io/blob/8f5fa805600f3ced73db5d134761ba91e8aea6ec/Screen%20Shot%202022-12-15%20at%2010.29.12%20PM.png)

## Casino Edge Prediction Model

```
deck_2 = casino_data.set_index("Decks").loc[2.0]
deck_2["Default Estimated Edge"] = 0.39
display(deck_2.head())

#Update Estimated Edge
for i in range(len(deck_2)):
  for rule in deck_2['Rules'].values[i]:
    temp = deck_2['Default Estimated Edge'].values[i]
    index = edge_ups[edge_ups['Rule'] == rule].index
    if len(edge_ups['2 Deck'].values[index]) > 0:
      temp2 = temp - edge_ups['2 Deck'].values[index][0]
      deck_2['Default Estimated Edge'].values[i] = temp2
    if rule == 'ls':
      if 'h17' in deck_2['Rules'].values[i]:
        deck_2['Default Estimated Edge'].values[i] = temp - edge_ups['2 Deck'].values[5]
      if 's17' in deck_2['Rules'].values[i]:
        deck_2['Default Estimated Edge'].values[i] = temp - edge_ups['2 Deck'].values[4]
display(deck_2.head())
```
<img width="844" alt="Screen Shot 2022-12-15 at 11 42 44 PM" src="https://user-images.githubusercontent.com/77644658/208030509-17739641-7433-410b-a9a3-b89f607f91e5.png">

```
deck_6 = casino_data.set_index("Decks").loc[6.0]
deck_6["Default Estimated Edge"] = 0.55
display(deck_6.head())

#Update Estimated Edge
for i in range(len(deck_6)):
  for rule in deck_6['Rules'].values[i]:
    temp = deck_6['Default Estimated Edge'].values[i]
    index = edge_ups[edge_ups['Rule'] == rule].index
    if len(edge_ups['6 Decks'].values[index]) > 0:
      temp2 = temp - edge_ups['6 Decks'].values[index][0]
      deck_6['Default Estimated Edge'].values[i] = temp2
    if rule == 'ls':
      if 'h17' in deck_6['Rules'].values[i]:
        deck_6['Default Estimated Edge'].values[i] = temp - edge_ups['6 Decks'].values[5]
      if 's17' in deck_6['Rules'].values[i]:
        deck_6['Default Estimated Edge'].values[i] = temp - edge_ups['6 Decks'].values[4]
display(deck_6.head())
```
<img width="832" alt="Screen Shot 2022-12-15 at 11 42 55 PM" src="https://user-images.githubusercontent.com/77644658/208030526-f854ec15-b4ad-4c60-9f6b-362807572ee7.png">

```
deck_8 = casino_data.set_index("Decks").loc[8.0]
deck_8["Default Estimated Edge"] = 0.56
display(deck_8.head())

#Update Estimated Edge
for i in range(len(deck_8)):
  for rule in deck_8['Rules'].values[i]:
    temp = deck_8['Default Estimated Edge'].values[i]
    index = edge_ups[edge_ups['Rule'] == rule].index
    if len(edge_ups['8 Decks'].values[index]) > 0:
      temp2 = temp - edge_ups['8 Decks'].values[index][0]
      deck_8['Default Estimated Edge'].values[i] = temp2
    if rule == 'ls':
      if 'h17' in deck_8['Rules'].values[i]:
        deck_8['Default Estimated Edge'].values[i] = temp - edge_ups['8 Decks'].values[5]
      if 's17' in deck_8['Rules'].values[i]:
        deck_8['Default Estimated Edge'].values[i] = temp - edge_ups['8 Decks'].values[4]
display(deck_8.head())
```
<img width="722" alt="Screen Shot 2022-12-15 at 11 43 04 PM" src="https://user-images.githubusercontent.com/77644658/208030544-8754c96e-495c-4d62-9872-7a2a36a57f77.png">

## Conclusion
