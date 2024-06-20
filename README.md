# TBC_final_project

# UI
This is CLI application

# Card Game "JOKER"

This is a Python implementation of the classic card game "JOKER". The game is played with a standard deck of 36 cards, where two Jokers substitute for the two black Sixes.

# Game Rules

The game is played among four players. It consists of four sets, with each set comprising four hands. In every hand, nine cards are dealt to each player. The dealing responsibility rotates clockwise, with the last player dealing cards in the first hand. After the cards are dealt, the player to the left of the dealer has the option to declare a trump suit or choose to play without a trump suit, based on their first three cards.

Players then proceed to bid on the number of tricks they believe they can win during that hand. Once the bidding is complete, the player to the dealer's left leads the first trick, setting the suit that must be followed by the other players. If a player cannot follow suit, they may play a card from the trump suit or a Joker card.

Points are awarded to players based on their bid and the actual number of tricks they won during the hand. A player who wins all their bids in one of the four sets receives a bonus. This bonus is an extra score equivalent to their highest score from any single hand in that set. The player with the highest cumulative score across all four sets emerges as the winner of the game.

_Rules for Placing a Bid:_

- Players must bid a number between 0 and 9, inclusive.
- The dealer cannot bid a number that would make the total sum of all bids equal to 9.

_Rules for Determining the Winning Card:_

- Joker is a winning card. If two jokers are played in the same trick, the second joker played wins.
- The highest trump card wins the trick, unless a joker is played.
- If all cards in a trick are of the same suit, the highest-ranking card wins, following the order: Ace, King, Queen, Jack, 10, 9, 8, 7, 6.

## Project Structure

The project is organized into the following modules:

- `main.py`: This is the entry point of the program. It initializes the game and starts the gameplay loop.
- `player.py`: This module contains the Player class, which represents a player in the game. It also includes a method to get the names of the players.
- `deck.py`: This module contains the Deck class, which represents the deck of cards. It handles the creation of the deck and the distribution of cards to the players.
- `hand.py`: This module contains the Hand class, which manages the gameplay of a single hand, including player bids, card plays, and scoring.
- `game.py`: This module contains the Game class, which represents the overall game and manages the game flow.

## Dependencies

This project uses the following Python libraries:

- `random`: Used for shuffling the deck and selecting random cards.
- `json`: Used for loading and saving game state.
- `prettytable`: Used for displaying scores in a tabular format (you may need to install this library separately if it's not already installed).
