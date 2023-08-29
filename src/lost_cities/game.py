import random
from typing import Any, Literal, Optional

from lost_cities import logger
from lost_cities.card import Card
from lost_cities.gui.settings import settings
from lost_cities.player import ComputerPlayer, Player


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
        self.deck: list[Card] = []
        self.discard_piles: list[Card] = []
        self.players: list[Player] = [Player(player1_name, version)]
        self.colors: list[str] = eval(f"self.VERSION_{version}")
        if vs_computer:
            self.players.append(ComputerPlayer(player2_name, version))
        else:
            self.players.append(Player(player2_name, version))
        self.current_player: int = 0

    def setup(self) -> None:
        """Sets all cards in the deck, shuffles and gives 8 cards for each player"""
        values = list(range(2, 11))  # Values from 2 to 10
        values.extend([0] * 3)  # 0 cards
        self.deck = [Card(color, value) for color in self.colors for value in values]
        random.shuffle(self.deck)

        for _ in range(8):
            for player in self.players:
                player.hand.append(self.deck.pop())

        self.players[0].reorder_hand()

    def switch_player(self) -> None:
        """Change player cursor"""
        self.current_player = 1 - self.current_player

    def pick_card(self, chosen_pile: Optional[str] = None) -> None:
        """Pick a card either in deck either in discard

        Args:
            chosen_pile (Optional[str], optional): chosen pile by compuyrt . Defaults to None.
        """
        current_player: Player = self.players[self.current_player]
        pile: str = chosen_pile or input("Choose a pile (deck/discard): ")
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

    def action_play_card(self, index: Optional[str] = None, skip_card: bool = False) -> bool:
        """Method to play a valid card

        Args:
            index (Optional[str]): if not None, index to take else would be asked with input. Defaults to None.
            skip_card (bool): Whether to skip last action as taking a card and switch player. Defaults to False.

        Returns:
            bool: Whether the card has been played
        """

        current_player: Player = self.players[self.current_player]
        card_input: str = index if index is not None else input("Index card to play: ")
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

        if skip_card is False:
            self.pick_card()
            self.switch_player()

        return can_play

    def action_discard(self, index: Optional[str] = None, skip_card: bool = False) -> None:
        """Method to discard a valid card

        Args:
            index (Optional[str]): if not None, index to take else would be asked with input. Defaults to None.
            skip_card (bool): Whether to skip last action as taking a card and switch player. Defaults to False.
        """

        current_player: Player = self.players[self.current_player]
        card_input: str = index if index is not None else input("Index card to discard: ")
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
        card.rotate_surface_to_discard()
        x, y = settings.discard_position
        card.set_coord(x, y)
        self.discard_piles.append(card)

        if skip_card is False:
            self.pick_card()
            self.switch_player()

    def play_round(
        self, action: Optional[str] = None, index: Optional[str] = None, skip_card: bool = False, gui: bool = False
    ) -> None:
        """Play a round. Player has to choose between play or discard then pick a card in deck or discard pile

        Args:
            action (Optional[str]): if not None, action to play else would be asked with input. Defaults to None.
            index (Optional[str]): if not None, index to take else would be asked with input. Defaults to None.
            skip_card (bool): Whether to skip last action as taking a card and switch player. Defaults to False.
            gui (bool): Whether playing gui. Defaults to False.

        """
        current_player: Player = self.players[self.current_player]

        logger.info(f"{current_player.name}'s turn.")

        if isinstance(current_player, ComputerPlayer):
            action, card = current_player.choose_action()
            if action == "play":
                current_player.play_card(card)
            else:
                discarded_card: Card = current_player.discard_card(card)
                discarded_card.rotate_surface_to_discard()
                self.discard_piles.append(discarded_card)

            last_discarded: Optional[Card] = None
            if len(self.discard_piles) > 0:
                last_discarded = self.discard_piles[-1]

            chosen_pile: str = current_player.choose_pile(last_discarded, action)
            self.pick_card(chosen_pile)
            self.switch_player()

        else:
            logger.info(f"Your hand: {[f'{i} = {card}' for i, card in enumerate(current_player.hand)]}")
            new_action = action or input("Choose an action (play/discard): ")
            while True:
                if new_action not in ["play", "discard"]:
                    logger.warning(f"{new_action} is not a valid action. Choose play or discard.")
                    new_action = input("Choose an action (play/discard): ")
                else:
                    break
            if new_action == "play":
                while True:
                    played: bool = self.action_play_card(index=index, skip_card=skip_card)
                    if played or gui:
                        break

            else:
                self.action_discard(index=index, skip_card=skip_card)

    def play_game(self) -> None:
        """Launch the game"""
        self.setup()

        while len(self.deck) != 0:
            self.play_round()

        scores: dict[str, Any] = {player.name: player.compute_score() for player in self.players}
        logger.info(f"Scores: {scores}")
        logger.info(f"Winner: {max(scores, key=scores.get)}")  # type: ignore


def main() -> None:  # pragma: nocover
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
