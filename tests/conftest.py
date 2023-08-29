import pygame
import pytest

from lost_cities.card import Card
from lost_cities.game import LostCitiesGame
from lost_cities.gui.gui import GUIGame
from lost_cities.player import ComputerPlayer, Player


@pytest.fixture
def test_player():
    return Player("Player1", version=5)


@pytest.fixture
def computer_player():
    cp = ComputerPlayer("Test Computer Player")
    cp.hand = [
        Card("Yellow", 0),
        Card("Yellow", 0),
        Card("Yellow", 2),
        Card("Yellow", 7),
        Card("Red", 8),
        Card("Green", 0),
        Card("Green", 5),
        Card("Green", 8),
    ]

    return cp


@pytest.fixture
def game_setup():
    game = LostCitiesGame("Player1", "Player2")
    game.setup()

    return game


@pytest.fixture
def gui_game():
    pygame.init()
    game = GUIGame()
    yield game
    pygame.quit()
