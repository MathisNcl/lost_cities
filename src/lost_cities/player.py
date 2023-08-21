from typing import Any

from lost_cities import logger
from lost_cities.card import Card


class Player:
    VERSION_5: list[str] = ["Yellow", "Blue", "White", "Green", "Red"]
    VERSION_6: list[str] = ["Yellow", "Blue", "White", "Green", "Red", "Purple"]

    def __init__(self, name: str, version: int = 5) -> None:
        """Initialisation of the player

        Args:
            name (str): Name of the player
            version (int): Number of colors possible, 5 or 6. Defaults to 5.
        """
        try:
            self.name: str = name
            self.hand: list = []
            self.board: dict = {color: [] for color in eval(f"self.VERSION_{version}")}
        except AttributeError:
            raise AttributeError("version should be 5 or 6 not {version}")

    def __repr__(self) -> str:
        """Representation of the object"""
        return f"{self.name} playing with {len(self.board)} colors\nActual setup: {self.board}"

    def play_card(self, card: Card) -> bool:
        """Play a card if possible and remove it from hand

        Args:
            card (Card): Card object to play

        Returns:
            bool: Whether the card can be play or not
        """
        # check whether it is allowed
        played: bool = False
        expedition: list = self.board[card.color]
        if len(expedition) == 0 or card.value >= expedition[-1]:
            self.hand.remove(card)
            self.board[card.color].append(card.value)
            played = True
            logger.info(f"{self.name} plays {str(card)}")
        else:
            logger.info(
                f"{self.name} can not play this card {card.value}:{card.color}"
                + f" because the last card is {self.board[card.color][-1]}"
            )

        return played

    def discard_card(self, card: Card) -> Card:
        """Remove a card from the hand

        Args:
            card (Card): Card to remove

        Returns:
            Card: Card removed
        """
        self.hand.remove(card)
        return card

    def reorder_hand(self) -> None:
        """Reorder the hand"""
        self.hand.sort()

    def compute_one_score(self, expedition: list) -> int:
        """Compute score for one expedition

        Args:
            expedition (list): value in the expedition

        Returns:
            int: score of the expedition
        """
        expedition_value: int = 0

        if len(expedition) > 0:
            paris_count = sum(value == 0 for value in expedition) + 1
            expedition_value = sum(value for value in expedition) - 20

            expedition_value *= paris_count
            if len(expedition) >= 8:
                expedition_value += 20

        return expedition_value

    def compute_score(self) -> tuple[int, dict]:
        """Compute final score

        Returns:
            tuple[int, dict]: final score from your board and detail by color
        """
        total_score: int = 0
        detail: dict = {}
        for color, expedition in self.board.items():
            expedition_value = self.compute_one_score(expedition)
            total_score += expedition_value

            detail[color] = expedition_value
        return total_score, detail


class ComputerPlayer(Player):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def __repr__(self) -> str:
        """Representation of the object"""
        return f"Computer named {self.name} playing with {len(self.board)} colors\nActual setup: {self.board}"

    def choose_action(self) -> tuple[str, Card]:
        # High importance rules
        for color in self.board:
            # Check if the player should start an expedition with a 0
            colored_hand: list[Card] = [card for card in self.hand if card.color == color]
            if (
                not self.board[color]
                and any(card.value == 0 for card in colored_hand)
                and (len(colored_hand) >= 4 or sum(card.value for card in colored_hand) >= 10)
            ):
                return ("play", Card(color, 0))

            # Play close card
            if self.board[color]:
                last_card_value: int = self.board[color][-1] if len(self.board[color]) > 0 else 0
                closest_card: list[bool] = [card.value == last_card_value + 1 for card in colored_hand]
                close_card: list[bool] = [card.value == last_card_value + 2 for card in colored_hand]
                if any(closest_card):
                    return ("play", Card(color, last_card_value + 1))
                elif any(close_card):
                    return ("play", Card(color, last_card_value + 2))

        # Medium importance rules
        for color in self.board:
            # Discard if many card not playable
            colored_hand = [card for card in self.hand if card.color == color]
            last_value: int = self.board[color][-1] if len(self.board[color]) > 0 else 0
            not_playable: list[Card] = [card for card in colored_hand if card.value < last_value]
            if len(not_playable) >= 3:
                return ("discard", not_playable[0])

        # Low importance
        best_move: dict[str, Any] = dict()
        for color in self.board:
            # play the closest
            colored_hand = [card for card in self.hand if card.color == color]
            last_value = self.board[color][-1] if len(self.board[color]) > 0 else 0
            playable: list[Card] = [card for card in colored_hand if card.value >= last_value]
            potential_diff: int = playable[0].value - last_value if len(playable) > 0 else 99
            if best_move.get("card") is None or best_move["diff"] > potential_diff:
                best_move = dict(card=playable[0], diff=potential_diff)
        return ("play", best_move["card"])
