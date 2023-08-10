import pytest
from lost_cities.player import Player


@pytest.fixture
def test_player():
    return Player("Player1", version=5)
