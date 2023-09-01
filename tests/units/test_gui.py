from lost_cities.gui.gui import GUIGame

# TODO: real tests not only launch test


def test_init(gui_game):
    assert isinstance(gui_game, GUIGame)

    assert gui_game.assets
    assert gui_game.pygame_objects
    assert gui_game.screen
    assert gui_game.font
    assert gui_game.end is False
    assert gui_game.last_action is None
    assert gui_game.running
    assert gui_game.rect_selected is None
    assert gui_game.selected_card is None
    assert gui_game.game


def test_process_without_event(gui_game):
    gui_game.can_i_play(nb_testing=5)
