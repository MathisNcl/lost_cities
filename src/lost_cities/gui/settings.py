from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 800
    CARD_WIDTH: int = 85
    CARD_HEIGHT: int = 133
    BOARD_WIDTH: int = 644
    BOARD_HEIGHT: int = 183

    # END layout
    END_WIDTH: int = SCREEN_WIDTH * 3 // 4
    END_HEIGHT: int = SCREEN_HEIGHT * 3 // 4
    END_X: int = (SCREEN_WIDTH - END_WIDTH) // 2
    END_Y: int = (SCREEN_HEIGHT - END_HEIGHT) // 2

    WHITE: tuple = (255, 255, 255)
    BLACK: tuple = (0, 0, 0)
    RED: tuple = (255, 0, 0)
    board_position: tuple = (
        int(SCREEN_WIDTH / 2 - BOARD_WIDTH / 2),
        int(SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2),  # - CARD_HEIGHT
    )

    PLAYER_HEIGHT_INIT: int = board_position[1] + BOARD_HEIGHT
    COMPUTER_HEIGHT_INIT: int = board_position[1] - CARD_HEIGHT

    pile_positions: dict[str, Any] = {
        "player": {
            "Yellow": (board_position[0] + 40, PLAYER_HEIGHT_INIT),
            "Blue": (board_position[0] + 160, PLAYER_HEIGHT_INIT),
            "White": (board_position[0] + 280, PLAYER_HEIGHT_INIT),
            "Green": (board_position[0] + 405, PLAYER_HEIGHT_INIT),
            "Red": (board_position[0] + 530, PLAYER_HEIGHT_INIT),
        },
        "computer": {
            "Yellow": (board_position[0] + 40, COMPUTER_HEIGHT_INIT),
            "Blue": (board_position[0] + 160, COMPUTER_HEIGHT_INIT),
            "White": (board_position[0] + 280, COMPUTER_HEIGHT_INIT),
            "Green": (board_position[0] + 405, COMPUTER_HEIGHT_INIT),
            "Red": (board_position[0] + 530, COMPUTER_HEIGHT_INIT),
        },
    }

    deck_position: tuple = (board_position[0] + 650, board_position[1])
    deck_text_position: tuple = (int(deck_position[0] + 50), int(deck_position[1] + 25))
    discard_position: tuple = (board_position[0] + 650, board_position[1] + CARD_WIDTH + 10)

    logo_play_position: tuple = (board_position[0] - 80, board_position[1])
    discard_play_position: tuple = (board_position[0] - 80, board_position[1] + CARD_WIDTH + 10)


settings = Settings()
