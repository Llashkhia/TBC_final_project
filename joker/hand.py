import json

CARD_COLORS = ["S", "H", "D", "C"]
CARD_VALUES = [6, 7, 8, 9, 10, "J", "Q", "K", "A"]


class Hand:
    def __init__(self, players_row, players_cards, trump):
        self.players_row = players_row
        self.players_cards = players_cards
        self.trump = trump
        self.players_points = {name: 0 for name in players_row.keys()}

    def get_word(self):
        players_bid = {}
        except_word = 0
        for name, number in sorted(self.players_row.items(), key=lambda x: x[1]):
            player_cards = self.players_cards[name]
            print(f"{name}'s CARDS: {player_cards}")
            word = -1
            if number == 4:
                while word < 0 or word > 9 or word == 9 - except_word:
                    try:
                        word = int(input(f"{name}, please enter your bid (0-9, but not {9 - except_word}): "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    if word < 0 or word > 9 or word == 9 - except_word:
                        print(f"Invalid bid. Please enter a number between 0 and 9, but not {9 - except_word}.")
            else:
                while word < 0 or word > 9:
                    try:
                        word = int(input(f"{name}, please enter your bid (0-9): "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                    if word < 0 or word > 9:
                        print("Invalid bid. Please enter a number between 0 and 9.")
            players_bid[name] = word
            except_word += word
        return players_bid

    def card_value(self, value):
        if isinstance(value, int):
            return value
        else:
            return {'J': 11, 'Q': 12, 'K': 13, 'A': 14}.get(value, 0)

    def lead_card(self, lead_player):
        players_lead = {}
        first_color = None
        joker_info = {'HIGH_LOW': None, 'color': None}
        players_order = list(self.players_row.keys())
        start_index = players_order.index(lead_player)

        for i in range(4):
            name = players_order[(start_index + i) % 4]
            player_cards = self.players_cards[name]
            print(f"{name}'s Cards: {player_cards}")

            valid_card = False
            while not valid_card:
                card_input = input(f"{name}, please play a card from your deck (e.g., 'S 10' or 'JOKER'): ").strip().upper()

                if card_input == 'JOKER' and 'JOKER' in player_cards:
                    if len(players_lead) == 0:  # first card
                        joker_act = input("Please enter 'HIGH' or 'LOW': ").strip().upper()
                        joker_color = input("Please enter color (S/H/D/C): ").strip().upper()
                        if joker_act in ['HIGH', 'LOW'] and joker_color in ['S', 'H', 'D', 'C']:
                            card = ('JOKER', joker_color, joker_act)
                            joker_info['HIGH_LOW'] = joker_act
                            joker_info['color'] = joker_color
                            first_color = joker_color
                            valid_card = True
                    else:
                        joker_act = input("Please enter 'HIGH' or 'LOW': ").strip().upper()
                        if joker_act in ['HIGH', 'LOW']:
                            card = ('JOKER', None, joker_act)
                            valid_card = True
                else:
                    try:
                        color, value = card_input.split()
                        if value.isdigit():
                            value = int(value)
                    
                        if (color, value) in player_cards:
                            filtered_list = filter(lambda card: isinstance(card, tuple) or card != 'JOKER', player_cards)
                            if first_color is None:
                                valid_card = True
                                first_color = color
                            elif color == first_color:
                                if joker_info['HIGH_LOW'] == 'HIGH' and i > 0:
                                    max_value = max(self.card_value(v) for c, v in filtered_list if c == first_color)
                                    if self.card_value(value) == max_value:
                                        valid_card = True
                                    else:
                                        print(f"You must play the highest card of {first_color}.")
                                else:
                                    valid_card = True
                            elif first_color not in [c for c, v in filtered_list]:
                                if self.trump is None or self.trump not in [c for c, v in filtered_list]:
                                    valid_card = True
                                elif color == self.trump:
                                    valid_card = True
                    except ValueError:
                        print("Invalid card input. Please enter in the format 'S 10' or 'JOKER'.")

                if valid_card:
                    if card_input == 'JOKER':
                        player_cards.remove('JOKER')
                        players_lead[name] = card
                    else:
                        player_cards.remove((color, value))
                        players_lead[name] = (color, value)
                else:
                    print("Invalid card. Please try again.")

            self.players_cards[name] = player_cards

        return players_lead, joker_info

    def compare_cards(self, players_lead, joker_info):
        def is_trump(card):
            if isinstance(card, tuple) and len(card) == 3 and card[0] == "JOKER":
                return False
            return card[0] == self.trump

        def is_joker(card):
            return isinstance(card, tuple) and len(card) == 3 and card[0] == "JOKER"

        def joker_details(card):
            if is_joker(card):
                return card[2], card[1]
            return None, None

        first_player = [name for name, number in self.players_row.items() if number == 1][0]
        first_player_card = players_lead[first_player]
        first_player_card_suit = first_player_card[0] if isinstance(first_player_card, tuple) else None

        winning_player = first_player
        winning_card = first_player_card

        for player, card in players_lead.items():
            if player == first_player:
                continue

            if is_joker(card):
                joker_act, joker_color = joker_details(card)
                if joker_act == 'HIGH':
                    if is_joker(winning_card):
                        if joker_info['HIGH_LOW'] == 'HIGH':
                            winning_player = player
                            winning_card = card
                    elif is_trump(winning_card):
                        if joker_color == self.trump or self.trump is None:
                            winning_player = player
                            winning_card = card
                    else:
                        winning_player = player
                        winning_card = card

            elif is_trump(card) and self.trump is not None:
                if is_joker(winning_card):
                    if joker_info['HIGH_LOW'] == 'HIGH' and joker_details(winning_card)[1] != self.trump:
                        winning_player = player
                        winning_card = card
                elif is_trump(winning_card):
                    if self.card_value(card[1]) > self.card_value(winning_card[1]):
                        winning_player = player
                        winning_card = card
                else:
                    winning_player = player
                    winning_card = card

            elif card[0] == first_player_card_suit:
                if not is_trump(winning_card) and not is_joker(winning_card) and self.card_value(card[1]) > self.card_value(winning_card[1]):
                    winning_player = player
                    winning_card = card

        if joker_info['HIGH_LOW'] == 'LOW' and is_joker(first_player_card):
            highest_card_player = max(
                [(p, c) for p, c in players_lead.items() if c[0] == joker_info['color'] and not is_joker(c)],
                key=lambda x: self.card_value(x[1][1]),
                default=(None, None)
            )[0]
            if highest_card_player:
                winning_player = highest_card_player
                winning_card = players_lead[highest_card_player]

        if not any(c[0] == first_player_card_suit for c in players_lead.values() if isinstance(c, tuple) and c != first_player_card) and (self.trump is None or not any(is_trump(c) for c in players_lead.values())):
            winning_player = first_player
            winning_card = first_player_card
        
        print(f'{winning_player} is the winner of the draw.')
        self.players_points[winning_player] += 1
        return winning_player

    def count_points(self, players_bid):
        try:
            with open("joker/points.json", "r") as file:
                point_values = json.load(file)
        except FileNotFoundError:
            print("No such file")

        players_scores = {}

        for name in players_bid.keys():
            if players_bid[name] == self.players_points[name]:  
                players_scores[name] = point_values[str(players_bid[name])]
            elif players_bid[name] != 0 and self.players_points[name] == 0:
                players_scores[name] = -500 
            else:
                players_scores[name] = self.players_points[name] * 10

        return players_scores
    