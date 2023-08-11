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


def test_player_discard(test_player):
    [test_player.hand.append(Card("Blue", i)) for i in range(2, 6)]

    assert len(test_player.hand) == 4

    discarded = test_player.discard_card(test_player.hand[2])

    assert len(test_player.hand) == 3
    assert all([card != discarded for card in test_player.hand])


@pytest.mark.parametrize("last_value,value", [(3, 4), (None, 4), (0, 4), (None, 0), (0, 0)])
def test_play_card_allowed(last_value, value, test_player, caplog):
    card = Card("Yellow", value)
    test_player.hand.append(card)
    if last_value is not None:
        test_player.board["Yellow"] = [last_value]
    result = test_player.play_card(card)
    assert result is True
    assert len(test_player.hand) == 0
    if last_value is None:
        assert test_player.board["Yellow"] == [value]
    else:
        assert test_player.board["Yellow"] == [last_value, value]
    assert f"Player1 plays {value}:Yellow" in caplog.text


@pytest.mark.parametrize("value", [0, 0])
def test_play_card_not_allowed(value, test_player, caplog):
    card = Card("Yellow", value)
    test_player.hand.append(card)
    test_player.board["Yellow"] = [0, 4]
    result = test_player.play_card(card)
    assert result is False
    assert len(test_player.hand) == 1
    assert test_player.board["Yellow"] == [0, 4]
    assert f"can not play this card {value}:Yellow because the last card is 4" in caplog.text


def test_compute_score(test_player):
    test_player.board["Yellow"] = [0, 3, 4, 6, 10]
    test_player.board["Blue"] = [6, 7]
    test_player.board["White"] = []
    test_player.board["Green"] = [3, 5, 7, 8, 9]
    test_player.board["Red"] = [0, 0, 0, 2, 4, 5, 8, 9]
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
