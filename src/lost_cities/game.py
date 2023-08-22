import random

from lost_cities.card import Card
from lost_cities.player import ComputerPlayer, Player
from typing import Literal, Optional
from lost_cities import logger


class LostCitiesGame:
    VERSION_5: list[str] = ["Yellow", "Blue", "White", "Green", "Red"]
    VERSION_6: list[str] = ["Yellow", "Blue", "White", "Green", "Red", "Purple"]

    def __init__(
        self, player1_name: str, player2_name: str, vs_computer: bool = True, version: Literal[5, 6] = 5
    ) -> None:
        """Constructor of a LostCities Game

        Args:
            player1_name (str): name of p1
            player2_name (str): name of p2
            vs_computer (bool, optional): Whether to play against computer. Defaults to True.
            version (Literal[5, 6], optional): Which version to play. Defaults to 5.
        """
        self.deck = []
        self.discard_piles = []
        self.players = [Player(player1_name, version)]
        self.colors = eval(f"self.VERSION_{version}")
        if vs_computer:
            self.players.append(ComputerPlayer(player2_name, version))
        else:
            self.players.append(Player(player2_name, version))
        self.current_player = 0

    def setup(self) -> None:
        """Sets all cards in the deck, shuffles and gives 8 cards for each player"""
        values = list(range(2, 11))  # Values from 2 to 10
        values.extend([0] * 3)  # 0 cards
        self.deck = [Card(color, value) for color in self.colors for value in values]
        random.shuffle(self.deck)

        for _ in range(8):
            for player in self.players:
                player.hand.append(self.deck.pop())

    def switch_player(self) -> None:
        """Change player cursor"""
        self.current_player = 1 - self.current_player

    def pick_card(self, chosen_pile: Optional[str] = None) -> None:
        """Pick a card either in deck either in discard

        Args:
            chosen_pile (Optional[str], optional): chosen pile by compuyrt . Defaults to None.
        """
        current_player: Player = self.players[self.current_player]
        pile: str = chosen_pile or input("Choose an pile (deck/discard): ")
        while True:
            if pile not in ["deck", "discard"]:
                logger.warning(f"{pile} is not a valid piles. Choose deck or discard.")
                pile = input("Choose a pile (deck/discard): ")
            elif pile == "discard" and len(self.discard_piles) == 0:
                logger.warning("No more card in discard, choose deck.")
                pile = "deck"
            else:
                break
        if pile == "deck":
            current_player.hand.append(self.deck.pop())
        else:
            current_player.hand.append(self.discard_piles.pop())
        current_player.reorder_hand()

    def action_play_card(self) -> bool:
        """Method to play a valid card

        Returns:
            bool: Whether the card has been played
        """

        current_player: Player = self.players[self.current_player]
        card_input: str = input("Index card to play: ")
        while True:
            try:
                card: Card = current_player.hand[int(card_input)]
                break
            except ValueError:
                logger.warning(f"{card_input} not a int.")
                card_input = input("Index card to play: ")
            except IndexError:
                logger.warning(f"{card_input} is not reachable. Choose a valid index from 0 to 7.")
                card_input = input("Index card to play: ")

        can_play: bool = current_player.play_card(card)
        if not can_play:
            return can_play

        self.pick_card()
        self.switch_player()

        return can_play

    def action_discard(self) -> None:
        """Method to discard a valid card"""

        current_player: Player = self.players[self.current_player]
        card_input: str = input("Index card to discard: ")
        while True:
            try:
                card: Card = current_player.hand[int(card_input)]
                break
            except ValueError:
                logger.warning(f"{card_input} not a int.")
                card_input = input("Index to discard: ")
            except IndexError:
                logger.warning(f"{card_input} is not reachable. Choose a valid index from 0 to 7.")
                card_input = input("Index to discard: ")

        current_player.discard_card(card)
        self.discard_piles.append(card)
        self.pick_card()
        self.switch_player()

    def play_round(self) -> None:
        """Play a round. Player has to choose between play or discard then pick a card in deck or discard pile"""
        current_player: Player = self.players[self.current_player]

        logger.info(f"{current_player.name}'s turn.")

        if isinstance(current_player, ComputerPlayer):
            action, card = current_player.choose_action()
            if action == "play":
                current_player.play_card(card)
            else:
                discarded_card: Card = current_player.discard_card(card)
                self.discard_piles.append(discarded_card)

            last_discarded: Optional[Card] = None
            if len(self.discard_piles) > 0:
                last_discarded = self.discard_piles[-1]

            chosen_pile: str = current_player.choose_pile(last_discarded, action)
            self.pick_card(chosen_pile)
            self.switch_player()

        else:
            logger.info(f"Your hand: {[f'{i} = {card}' for i, card in enumerate(current_player.hand)]}")
            action = input("Choose an action (play/discard): ")
            while True:
                if action not in ["play", "discard"]:
                    logger.warning(f"{action} is not a valid action. Choose play or discard.")
                    action = input("Choose an action (play/discard): ")
                else:
                    break
            if action == "play":
                while True:
                    played: bool = self.action_play_card()
                    if played:
                        break

            else:
                self.action_discard()

    def play_game(self) -> None:
        """Launch the game"""
        self.setup()

        while len(self.deck) != 0:
            self.play_round()

        scores: dict[str, int] = {player.name: player.compute_score() for player in self.players}
        logger.info(f"Scores: {scores}")
        logger.info(f"Winner: {max(scores, key=scores.get)}")


def main():  # pragma: nocover
    name1: str = input("Name of Player 1? ")
    vs_computer_Yn: str = input("Play against computer? (Y/n): ")
    vs_computer: bool = True
    name2: str = "Ordi"
    if vs_computer_Yn.upper() != "Y":
        vs_computer = False
        name2 = input("Name of Player 2? ")

    game = LostCitiesGame(name1, name2, vs_computer=vs_computer)
    game.play_game()


if __name__ == "__main__":  # pragma: nocover
    main()
