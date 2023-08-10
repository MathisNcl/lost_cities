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
            self.board: dict = {color: [0] for color in eval(f"self.VERSION_{version}")}
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
        if (
            card.value == "Paris"
            and self.board[card.color][-1] in [0, "Paris"]
            or int(card.value) > int(self.board[card.color][-1])  # FIXME: should bug
        ):
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

    def compute_one_score(self, expedition: list) -> int:
        expedition_value: int = 0

        if len(expedition) > 1:
            paris_count = sum(value == "Bet" for value in expedition) + 1
            expedition_value = sum(int(value) for value in expedition if value != "Bet") - 20

            expedition_value *= paris_count
            if len(expedition) >= 9:
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
    def __init__(self, name):
        super().__init__(name)

    def choose_action(self):
        # Check if the player can start an expedition
        for color in self.board:
            if not self.board[color] and (
                any(card.value == "Bet" for card in self.hand)
                and (
                    sum(card.color == color for card in self.hand) >= 3
                    or sum(card.value for card in self.hand if card.color == color) >= 10
                )
            ):
                return ("play",)  # self.hand.index("Bet") change to get the  first bet from the color

        # Play close card
        for color in self.board:
            if len(self.board[color]) > 1:
                last_card_value = self.board[color][-1].value
                close_card = [card.value == last_card_value + 1 for card in self.hand if card.color == color]
                if last_card_value != "Paris" and any(close_card):
                    return ("play", color, close_card)

    def calculate_potential_score(self, color, expedition):
        play_score = self.compute_one_score(expedition)

        discard_score = 0
        for card in self.hand:
            if card.color == color:
                discard_score += card.value - 20
                if card.value == "Paris":
                    discard_score *= 2

        return {"play": play_score, "discard": discard_score}
