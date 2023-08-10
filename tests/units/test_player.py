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
    assert all([len(values) == 1 and values[-1] == 0 for _, values in test_player.board.items()])
    assert test_player.hand == []
    assert test_player.name == "Player1"
    assert f"{test_player.name} playing with {len(test_player.board)} colors\nActual setup:" in str(test_player)


def test_player_discard(test_player):
    [test_player.hand.append(Card("Blue", str(i))) for i in range(2, 6)]

    assert len(test_player.hand) == 4

    discarded = test_player.discard_card(test_player.hand[2])

    assert len(test_player.hand) == 3
    assert all([card != discarded for card in test_player.hand])


def test_play_card_allowed(test_player, caplog):
    card = Card("Yellow", "3")
    test_player.hand.append(card)
    result = test_player.play_card(card)
    assert result is True
    assert len(test_player.hand) == 0
    assert test_player.board["Yellow"] == [0, "3"]
    assert "Player1 plays 3:Yellow" in caplog.text


def test_play_card_not_allowed(test_player, caplog):
    card = Card("Yellow", "3")
    test_player.hand.append(card)
    test_player.board["Yellow"] = [0, "4"]
    result = test_player.play_card(card)
    assert result is False
    assert len(test_player.hand) == 1
    assert test_player.board["Yellow"] == [0, "4"]
    assert "can not play this card 3:Yellow because the last card is 4" in caplog.text


def test_compute_score(test_player):
    test_player.board["Yellow"] = [0, "Bet", "3", "4", "6", "10"]
    test_player.board["Blue"] = [0, "6", "7"]
    test_player.board["White"] = [0]
    test_player.board["Green"] = [0, "3", "5", "7", "8", "9"]
    test_player.board["Red"] = [0, "Bet", "Bet", "Bet", "2", "4", "5", "8", "9"]
    score, detail = test_player.compute_score()
    assert score == 63
    assert detail["Yellow"] == 6
    assert detail["Blue"] == -7
    assert detail["White"] == 0
    assert detail["Green"] == 12
    assert detail["Red"] == 52
