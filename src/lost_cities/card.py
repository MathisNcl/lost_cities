from typing import Any

import numpy as np
import pygame

from lost_cities.gui.utils import extract_card


class Card:
    def __init__(self, color: str, value: int, x: int = 0, y: int = 0) -> None:
        """Instanciate Card

        Args:
            color (str): color of the card
            value (int): value of the card
            x (int): x coord board
            y (int): y coord board
        """
        if color not in ["Yellow", "Blue", "White", "Green", "Red", "Purple"]:
            raise AttributeError(f"color can not be {color}")
        if value not in [i for i in range(2, 11)] and value != 0:
            raise AttributeError("value must be between 2 and 10 or a 0")
        self.color = str(color)
        self.value = value
        self.img = extract_card(self.color, self.value)
        self.surface = pygame.pixelcopy.make_surface(np.flipud(np.rot90(self.img)))
        self.x = x
        self.y = y
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)

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

    def rotate_surface_to_discard(self) -> None:
        """change surface value to rotate for discard view"""
        self.surface = pygame.pixelcopy.make_surface(np.flipud(self.img))

    def unrotate_surface_to_discard(self) -> None:
        """change surface value to unrotate for hand view"""
        self.surface = pygame.pixelcopy.make_surface(np.flipud(np.rot90(self.img)))

    def set_coord(self, x: int, y: int) -> None:
        """Set x and y coord for pygame view

        Args:
            x (int): x coord
            y (int): y coord
        """
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)
