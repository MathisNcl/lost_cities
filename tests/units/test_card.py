import pytest

from lost_cities.card import Card
import numpy as np


@pytest.mark.parametrize("color,value", [("Blue", 9), ("Yellow", 2), ("Red", 0)])
def test_card(color, value):
    card = Card(color, value)
    assert card.color == color
    assert card.value == value
    assert str(card) == f"{value}:{color}"
    assert isinstance(card.img, np.ndarray)
    assert card.img.shape[0:2] == (133, 85)


def test_card_error():
    with pytest.raises(AttributeError) as e:
        Card("dummy", "6")
        assert "color can not be" in e

    with pytest.raises(AttributeError) as e:
        Card("Blue", "dummy")
        assert "value must be between 2 and 10 or a 0" in e
