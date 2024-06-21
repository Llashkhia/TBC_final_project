import json
from player import Player
from deck import Deck
from hand import Hand
from prettytable import PrettyTable

class Game:
    def __init__(self):
        self.players = Player.get_players_name(self)
        self.deck = Deck()
        self.starting_player_index = 0
        self.overall_scores = {player.name: 0 for player in self.players}
        self.game_table = PrettyTable([player.name for player in self.players])

    def play(self):
        print(f'\nWe have four players in the game: {', '.join(player.name for player in self.players)}')
        for hand_set in range(4):
            self.play_hand_set(hand_set)

        self.display_final_scores(self.players, self.overall_scores)
        self.save_game(self.overall_scores, 0, 0)

    def row_of_players(names, start_index=0):
        players_num = {}
        for i, name in enumerate(names):
            players_num[name] = (start_index + i) % 4 + 1
        return players_num

    def play_hand(self, hand):
        print(f"\nHand {hand + 1}\n")

        players_row = Game.row_of_players([player.name for player in self.players], self.starting_player_index)
        players_cards = self.deck.generate_cards(self.players)
        trump = self.deck.trump_suit(players_row, players_cards)

        hand_instance = Hand(players_row, players_cards, trump)
        players_bid = hand_instance.get_word()

        lead_player = [name for name, number in players_row.items() if number == 1][0]

        for draw in range(9):
            print(f"\nDraw {draw + 1}")
            players_lead, joker_info = hand_instance.lead_card(lead_player)
            lead_player = hand_instance.compare_cards(players_lead, joker_info)

        players_scores = hand_instance.count_points(players_bid)

        self.game_table.add_row([f"{players_bid[player.name]}:{players_scores[player.name]}" for player in self.players])

        print(self.game_table)
        
        for player in self.players:
            self.overall_scores[player.name] += players_scores[player.name]

        return {player.name: {'bid': players_bid[player.name], 'taken': hand_instance.players_points[player.name], 'score': players_scores[player.name]} for player in self.players}

    def play_hand_set(self, hand_set):
        print(f"\nStarting Hand Set {hand_set + 1}\n")
        hand_scores = []
        set_scores = {player.name: 0 for player in self.players}

        for hand in range(4):
            hand_score = self.play_hand(hand)
            hand_scores.append(hand_score)
            for player in self.players:
                set_scores[player.name] += hand_score[player.name]['score']
            self.starting_player_index = (self.starting_player_index - 1) % 4  # Rotate the starting player

        self.apply_set_bonus(self.players, self.overall_scores, hand_scores)

        
        self.game_table.add_row([f"{set_scores[player.name]}" for player in self.players], divider= True)
        self.game_table.add_row([f"{self.overall_scores[player.name]}" for player in self.players], divider= True)
        
        print()
        print(self.game_table)

    def apply_set_bonus(self, players, overall_scores, hand_scores):
        for player in players:
            if all(hand_scores[hand][player.name]['bid'] == hand_scores[hand][player.name]['taken'] for hand in range(4)):
                max_score = max(hand_scores[hand][player.name]['score'] for hand in range(4))
                last_score = hand_scores[3][player.name]['score']
                bonus_score = max_score + last_score
                overall_scores[player.name] += bonus_score
                print(f"{player.name} gets a bonus score of {bonus_score} for having all bids equal to taken points.")

    def save_game(self, players_scores: dict, current_four: int, current_hand: int):
        game_state = {
            'scores': players_scores,
            'current_four': current_four,
            'current_hand': current_hand,
            'final_table': str(self.game_table)
        }
        try:
            with open("joker/game_scores.json", 'w') as file:
                json.dump(game_state, file)
            print(f"Game state saved to joker/game_scores.json")
        except IOError as e:
            print(f"An error occurred while saving the game state: {e}")


    def load_game(file_name: str = 'joker/game_scores.json') -> dict:
        try:
            with open(file_name, 'r') as file:
                players_scores = json.load(file)
            print(f"Game state loaded from {file_name}")
            return players_scores
        except FileNotFoundError:
            print(f"No such file: {file_name}")
            return {}
        except IOError as e:
            print(f"An error occurred while loading the game state: {e}")
            return {}

    def display_final_scores(self, players, overall_scores):
        self.game_table.field_names = [player.name for player in players]
        self.game_table.add_row([f"{overall_scores[player.name]}" for player in players])

        print(self.game_table)
