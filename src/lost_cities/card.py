from typing import Any


class Card:
    def __init__(self, color: str, value: int) -> None:
        """Instanciate Card

        Args:
            color (str): color of the card
            value (int): value of the card
        """
        if color not in ["Yellow", "Blue", "White", "Green", "Red", "Purple"]:
            raise AttributeError(f"color can not be {color}")
        if value not in [i for i in range(2, 11)] and value != 0:
            raise AttributeError("value must be between 2 and 10 or a 0")
        self.color = str(color)
        self.value = value

    def __repr__(self) -> str:
        """Representation of a card

        Returns:
            str
        """
        return f"{self.value}:{self.color}"

    def __lt__(self, card: Any) -> bool:
        """lower than, used to sort list

        Args:
            card (Any): card to compare with

        Returns:
            bool: if this card is lower than a given card
        """
        return self.color < card.color or self.color == card.color and self.value < card.value

    def __eq__(self, card: Any) -> bool:
        """equal to

        Args:
            card (Any): card to compare with

        Returns:
            bool: if this card is equal to a given card
        """
        return self.color == card.color and self.value == card.value
