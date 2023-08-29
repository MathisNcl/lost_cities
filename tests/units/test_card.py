import numpy as np
import pygame
import pytest

from lost_cities.card import Card


@pytest.mark.parametrize("color,value", [("Blue", 9), ("Yellow", 2), ("Red", 0)])
def test_card(color, value):
    card = Card(color, value)
    assert card.color == color
    assert card.value == value
    assert str(card) == f"{value}:{color}"
    assert isinstance(card.img, np.ndarray)
    assert card.img.shape[0:2] == (133, 85)
    assert isinstance(card.surface, pygame.Surface)
    assert card.surface.get_size() == (85, 133)
    assert isinstance(card.rect, pygame.Rect)
    assert card.rect.size == (85, 133)
    assert card.x == 0
    assert card.y == 0


def test_card_rotate():
    card = Card("Blue", 0)
    card.rotate_surface_to_discard()
    assert isinstance(card.surface, pygame.Surface)
    assert card.surface.get_size() == (133, 85)

    card.unrotate_surface_to_discard()
    assert isinstance(card.surface, pygame.Surface)
    assert card.surface.get_size() == (85, 133)


def test_card_set_coord():
    card = Card("Blue", 0)
    assert card.x == 0
    assert card.y == 0

    card.set_coord(100, 100)
    assert card.x == 100
    assert card.y == 100


def test_card_error():
    with pytest.raises(AttributeError) as e:
        Card("dummy", "6")
        assert "color can not be" in e

    with pytest.raises(AttributeError) as e:
        Card("Blue", "dummy")
        assert "value must be between 2 and 10 or a 0" in e
