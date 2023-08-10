import random

from lost_cities.card import Card
from lost_cities.player import ComputerPlayer, Player


class LostCitiesGame:
    def __init__(self, player1_name, player2_name):
        self.deck = []
        self.discard_piles = {color: [] for color in ["Yellow", "Blue", "White", "Green", "Red"]}
        self.players = [Player(player1_name), Player(player2_name)]
        self.current_player = 0

    def setup(self):
        colors = ["Yellow", "Blue", "White", "Green", "Red"]
        values = list(range(2, 11))  # Values from 2 to 10
        values.extend(["Paris"] * 3)  # Paris cards
        self.deck = [Card(color, value) for color in colors for value in values]
        random.shuffle(self.deck)

        for _ in range(8):
            for player in self.players:
                player.hand.append(self.deck.pop())

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def play_round(self):
        current_player = self.players[self.current_player]

        print(f"{current_player.name}'s turn.")
        print(f"Your hand: {[str(card) for card in current_player.hand]}")

        if isinstance(current_player, ComputerPlayer):
            action, color = current_player.choose_action()
            if action == "play":
                print(f"{current_player.name} plays {color}.")
                current_player.play_card(current_player.hand[0], color)
            else:
                print(f"{current_player.name} discards a card.")
                discarded_card = current_player.hand[0]
                current_player.hand.remove(discarded_card)
                self.discard_piles[discarded_card.color].append(discarded_card)
        else:
            action = input("Choose an action (play/discard): ")

            if action == "play":
                expedition_color = input("Choose an expedition color (Yellow, Blue, White, Green, Red): ")
                card_index = int(input("Choose a card to play (index): "))

                card = current_player.hand[card_index]

                if card in current_player.hand:
                    current_player.play_card(card, expedition_color)
                    current_player.hand.pop(card_index)  # Remove card from hand
                    self.switch_player()
                else:
                    print("Invalid card selection. Try again.")
            elif action == "discard":
                card_index = int(input("Choose a card to discard (index): "))

                card = current_player.hand[card_index]

                if card in current_player.hand:
                    discarded_card = current_player.hand.pop(card_index)  # Remove card from hand
                    self.discard_piles[card.color].append(discarded_card)  # Discard card
                    new_card = self.deck.pop()  # Draw a new card from deck
                    current_player.hand.append(new_card)
                    self.switch_player()
                else:
                    print("Invalid card selection. Try again.")
            else:
                print("Invalid action. Try again.")

    def play_game(self) -> None:
        self.setup()

        for _ in range(16):  # 3 rounds * 2 players + 1
            self.play_round()

        for player in self.players:
            print(f"{player.name}'s score: {player.calculate_score()}")
