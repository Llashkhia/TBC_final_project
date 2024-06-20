import random

CARD_COLORS = ["S", "H", "D", "C"]
CARD_VALUES = [6, 7, 8, 9, 10, "J", "Q", "K", "A"]


class Deck:
    def __init__(self):
        self.deck = self.create_deck(CARD_COLORS, CARD_VALUES)

    def create_deck(self, colors, values):
        deck = [(color, value) for color in colors for value in values
                if not (color == "S" and value == 6) and not (color == "C" and value == 6)]
        deck.append("JOKER")
        deck.append("JOKER")
        return deck

    def generate_cards(self, players):
        if not self.deck:  # Check if the deck is empty
            self.deck = self.create_deck(CARD_COLORS, CARD_VALUES)  # Recreate the deck if it's empty

        players_cards = {}
        for player in players:
            player_cards = []
            for _ in range(9):
                if not self.deck:
                    break  
                card = random.choice(self.deck)
                player_cards.append(card)
                self.deck.remove(card)
            players_cards[player.name] = player_cards
        return players_cards
    
    def trump_suit(self, players_row, players_cards):
        for name, number in players_row.items():
            if number == 1:
                first_player = name
        first_player_cards = players_cards[first_player]
        first_three_cards = first_player_cards[:3]

        print(f"{first_player}'s first three cards are: {first_three_cards}")
        while True:
            trump = input("Please choose a trump suit ('S', 'H', 'D', 'C'). If you don't want a trump suit, enter '-': ").strip().upper()

            if trump == "-":
                return None
            elif trump in CARD_COLORS:
                return trump
            else:
                print("Incorrect input. Please try again.")
                