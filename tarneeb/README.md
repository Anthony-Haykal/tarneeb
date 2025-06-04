# Tarneeb Card Game

A digital implementation of the popular Middle Eastern trick-taking card game "Tarneeb" (طرنيب), built with Python and Pygame.

## Game Overview

Tarneeb is a 4-player card game played with a standard 52-card deck where players form two teams. The goal is to win tricks and reach a target score before the opposing team.

## Features

- Complete implementation of Tarneeb rules
- Intuitive GUI with card animations
- AI opponents with bidding and playing strategies
- Team play (2 vs 2)
- Score tracking

## Game Rules

1. **Objective**: The objective is to win tricks containing valuable cards. Teams try to reach the target score (default: 31 points) first.

2. **Bidding Phase**: 
   - Players bid on the number of tricks they think their team can win (minimum 7, maximum 13)
   - The highest bidder chooses the trump suit
   - If a team fails to achieve its bid, they lose points equal to their bid

3. **Trick-Taking Phase**:
   - Players must follow the lead suit if possible
   - If a player can't follow suit, they can play any card (including a trump)
   - The highest card of the leading suit wins unless a trump card is played
   - If multiple trump cards are played, the highest trump wins

4. **Scoring**:
   - If the bidding team makes or exceeds their bid, they score the number of tricks they won
   - If they fail, they lose the bid amount
   - The opposing team always scores the number of tricks they won




## Controls

- During bidding:
  - Click on a bid value (7-13) or "Pass"
  - Select a trump suit
  - Confirm your selection
  
- During play:
  - Click on a valid card to play it
  - The game will highlight valid cards based on the rules

