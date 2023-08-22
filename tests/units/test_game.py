from unittest.mock import patch

from lost_cities.card import Card
from lost_cities.game import LostCitiesGame
from lost_cities.player import ComputerPlayer

initial_hand_size: int = 8
initial_deck_size: int = 44


def test_setup():
    game = LostCitiesGame("Player1", "Player2", vs_computer=False)
    game.setup()

    total_cards_in_hands = sum(len(player.hand) for player in game.players)
    assert total_cards_in_hands == 16  # 8 cards per player

    assert len(game.deck) == 60 - total_cards_in_hands
    assert len(game.discard_piles) == 0

    # Check that cards are not ordered (shuffle)
    cards_in_order = all(
        game.deck[i].color == game.colors[i // 10] and game.deck[i].value == (i % 10) + 2 for i in range(len(game.deck))
    )
    assert not cards_in_order


def test_setup_vs_computer():
    game = LostCitiesGame("Player1", "Player2")
    game.setup()

    total_cards_in_hands = sum(len(player.hand) for player in game.players)
    assert total_cards_in_hands == 16  # 8 cards per player

    assert len(game.deck) == 60 - total_cards_in_hands
    assert len(game.discard_piles) == 0

    # Check that cards are not ordered (shuffle)
    cards_in_order = all(
        game.deck[i].color == game.colors[i // 10] and game.deck[i].value == (i % 10) + 2 for i in range(len(game.deck))
    )
    assert not cards_in_order


@patch("builtins.input", side_effect=["dummy", "deck"])
def test_pick_card_deck(mock_input, game_setup, caplog):
    game_setup.pick_card()

    assert "dummy is not a valid piles. Choose deck or discard." in caplog.text

    assert len(game_setup.deck) == initial_deck_size - 1
    assert len(game_setup.players[0].hand) == initial_hand_size + 1


@patch("builtins.input", side_effect=["discard"])
def test_pick_discard_empty(mock_input, game_setup, caplog):
    assert len(game_setup.discard_piles) == 0
    game_setup.pick_card()

    assert "No more card in discard, choose deck." in caplog.text

    assert len(game_setup.deck) == initial_deck_size - 1
    assert len(game_setup.discard_piles) == 0
    assert len(game_setup.players[0].hand) == initial_hand_size + 1


@patch("builtins.input", side_effect=["discard"])
def test_pick_card_discard(mock_input, game_setup):
    game_setup.discard_piles = [Card("Yellow", 10)]
    initial_discard_piles_size = 1
    game_setup.pick_card()

    assert len(game_setup.discard_piles) == initial_discard_piles_size - 1
    assert len(game_setup.players[0].hand) == initial_hand_size + 1


@patch("builtins.input", side_effect=["0"])
def test_action_play_card_not_playable(mock_input, game_setup, caplog):
    game_setup.players[0].hand[0] = Card("Red", 3)
    game_setup.players[0].board["Red"] = [4]

    assert game_setup.action_play_card() is False

    assert "can not play this card 3:Red because the last card is 4" in caplog.text


def test_game_only_computers(caplog):
    game = LostCitiesGame("ORDI1", "ORDI2")
    game.players[0] = ComputerPlayer("ORDI1")

    game.play_game()

    assert "Winner" in caplog.text
    assert len(game.deck) == 0


@patch("builtins.input", side_effect=["dummy", "play", "10", "dummy", "0", "deck"])
def test_play_round(mock_input, game_setup, caplog):
    first_card = game_setup.players[0].hand[0]
    game_setup.play_round()

    assert "Your hand" in caplog.text
    assert "dummy is not a valid action. Choose play or discard." in caplog.text

    assert "not a int" in caplog.text
    assert "not reachable" in caplog.text

    assert len(game_setup.players[0].hand) == initial_hand_size
    assert first_card != game_setup.players[0].hand[0]
    assert first_card.value in game_setup.players[0].board[first_card.color]

    assert len(game_setup.deck) == initial_deck_size - 1

    assert game_setup.current_player == 1


@patch("builtins.input", side_effect=["discard", "10", "dummy", "0", "deck"])
def test_play_round_discard(mock_input, game_setup, caplog):
    game_setup.discard_piles.append(Card("Yellow", 10))
    first_card = game_setup.players[0].hand[0]
    game_setup.play_round()

    assert "Your hand" in caplog.text
    assert "not a int" in caplog.text
    assert "not reachable" in caplog.text

    assert len(game_setup.players[0].hand) == initial_hand_size
    assert len(game_setup.discard_piles) == 2
    assert game_setup.discard_piles[-1] == first_card

    assert game_setup.current_player == 1
