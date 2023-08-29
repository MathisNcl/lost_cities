import pytest

from lost_cities.card import Card
from lost_cities.player import Player


@pytest.mark.parametrize("version", ["dummy", 7, 1, 4])
def test_player_instanciate_error(version):
    with pytest.raises(AttributeError) as e:
        Player("Dummy", version)
        assert "version should be 5 or 6 not" in e


def test_player_instanciate(test_player):
    assert len(test_player.board) == 5
    assert all([len(values) == 0 for _, values in test_player.board.items()])
    assert test_player.hand == []
    assert test_player.name == "Player1"
    assert f"{test_player.name} playing with {len(test_player.board)} colors\nActual setup:" in str(test_player)


def test_player_discard(test_player, caplog):
    [test_player.hand.append(Card("Blue", i)) for i in range(2, 6)]

    assert len(test_player.hand) == 4

    discarded = test_player.discard_card(test_player.hand[2])

    assert len(test_player.hand) == 3
    assert all([card != discarded for card in test_player.hand])

    assert "discard" in caplog.text


@pytest.mark.parametrize("last_value,value", [(3, 4), (None, 4), (0, 4), (None, 0), (0, 0)])
def test_play_card_allowed(last_value, value, test_player, caplog):
    card = Card("Yellow", value)
    test_player.hand.append(card)
    if last_value is not None:
        test_player.board["Yellow"] = [Card("Yellow", last_value)]
    result = test_player.play_card(card)
    assert result is True
    assert len(test_player.hand) == 0
    if last_value is None:
        assert test_player.board["Yellow"] == [Card("Yellow", value)]
    else:
        assert test_player.board["Yellow"] == [Card("Yellow", last_value), Card("Yellow", value)]
    assert f"Player1 plays {value}:Yellow" in caplog.text


@pytest.mark.parametrize("value", [0, 0])
def test_play_card_not_allowed(value, test_player, caplog):
    card = Card("Yellow", value)
    test_player.hand.append(card)
    test_player.board["Yellow"] = [Card("Yellow", 0), Card("Yellow", 4)]
    result = test_player.play_card(card)
    assert result is False
    assert len(test_player.hand) == 1
    assert test_player.board["Yellow"] == [Card("Yellow", 0), Card("Yellow", 4)]
    assert f"can not play this card {value}:Yellow because the last card is 4" in caplog.text


def test_compute_score(test_player):
    board = {
        "Yellow": [0, 3, 4, 6, 10],
        "Blue": [6, 7],
        "White": [],
        "Green": [3, 5, 7, 8, 9],
        "Red": [0, 0, 0, 2, 4, 5, 8, 9],
    }

    test_player.board = {color: [Card(color, value) for value in values] for color, values in board.items()}
    score, detail = test_player.compute_score()
    assert score == 63
    assert detail["Yellow"] == 6
    assert detail["Blue"] == -7
    assert detail["White"] == 0
    assert detail["Green"] == 12
    assert detail["Red"] == 52


def test_reorder_hand(test_player):
    test_player.hand = [Card("Yellow", 7), Card("Yellow", 0), Card("Blue", 4), Card("Blue", 2), Card("Red", 10)]

    test_player.reorder_hand()

    assert test_player.hand == [Card("Blue", 2), Card("Blue", 4), Card("Red", 10), Card("Yellow", 0), Card("Yellow", 7)]


# ================================
# Computer


def test_computer_player_instanciate(computer_player):
    assert len(computer_player.board) == 5
    assert all([len(values) == 0 for _, values in computer_player.board.items()])
    assert len(computer_player.hand) == 8
    assert computer_player.name == "Test Computer Player"
    assert (
        f"Computer named {computer_player.name} playing with {len(computer_player.board)} colors\nActual setup:"
        in str(computer_player)
    )


@pytest.mark.parametrize(
    "board, expected_action",
    [
        ({"Yellow": [4]}, ("play", Card("Green", 0))),
        ({"Green": []}, ("play", Card("Yellow", 0))),
        ({"Green": [2, 4], "Yellow": [4]}, ("play", Card("Green", 5))),
        ({"Red": [2, 5, 6], "Green": [2, 4, 9], "Yellow": [4]}, ("play", Card("Red", 8))),
    ],
)
def test_choose_action_high_importance(computer_player, board, expected_action):
    board = {color: [Card(color, value) for value in values] for color, values in board.items()}
    computer_player.board.update(board)
    action = computer_player.choose_action()
    assert action == expected_action


@pytest.mark.parametrize(
    "board, expected_action",
    [
        ({"Green": [2], "Yellow": [8]}, ("discard", Card("Yellow", 0))),
        ({"Green": [10], "Yellow": [2]}, ("discard", Card("Green", 0))),
    ],
)
def test_choose_action_medium_importance(computer_player, board, expected_action):
    board = {color: [Card(color, value) for value in values] for color, values in board.items()}
    computer_player.board.update(board)
    action = computer_player.choose_action()
    assert action == expected_action


@pytest.mark.parametrize(
    "board, expected_action",
    [
        ({"Green": [3, 4], "Yellow": [2], "Red": [5]}, ("play", Card("Red", 8))),
        ({"Green": [10], "Yellow": [2]}, ("play", Card("Yellow", 7))),
        ({"Green": [10], "Yellow": [8]}, ("discard", Card("Yellow", 0))),
        ({"Green": [10], "Yellow": [10], "Red": [10]}, ("discard", Card("Yellow", 0))),
    ],
)
def test_choose_action_low_importance(computer_player, board, expected_action):
    board = {color: [Card(color, value) for value in values] for color, values in board.items()}
    computer_player.board.update(board)
    computer_player.discard_card(Card("Yellow", 2))
    if computer_player.board["Yellow"] == [Card("Yellow", 10)]:
        computer_player.discard_card(Card("Yellow", 0))
    computer_player.discard_card(Card("Green", 5))
    action = computer_player.choose_action()
    assert action == expected_action


@pytest.mark.parametrize(
    "discard_card, last_action, expected_choice",
    [
        (None, "discard", "deck"),
        (Card("Green", 0), "play", "discard"),
        (Card("Green", 0), "discard", "deck"),
        (Card("Red", 7), "play", "discard"),
        (Card("Red", 2), "play", "deck"),
        (Card("Blue", 9), "play", "discard"),
        (Card("Blue", 4), "play", "deck"),
    ],
)
def test_player_choose_pile(computer_player, discard_card, last_action, expected_choice):
    computer_player.hand = [
        Card("Yellow", 0),
        Card("Yellow", 2),
        Card("Yellow", 7),
        Card("Red", 8),
        Card("Green", 0),
        Card("Green", 5),
        Card("Green", 8),
    ]
    computer_player.board = {
        "Yellow": [],
        "Blue": [Card("Blue", 3), Card("Blue", 5), Card("Blue", 6)],
        "Red": [],
        "Green": [],
        "White": [],
    }
    result = computer_player.choose_pile(discard_card, last_action)
    assert result == expected_choice
