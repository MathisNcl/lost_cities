from pydantic_settings import BaseSettings
from typing import Any


class Settings(BaseSettings):
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 800
    CARD_WIDTH: int = 85
    CARD_HEIGHT: int = 133
    BOARD_WIDTH: int = 644
    BOARD_HEIGHT: int = 183

    WHITE: tuple = (255, 255, 255)
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
    discard_position: tuple = (board_position[0] + 650, board_position[1] + CARD_WIDTH + 10)


settings = Settings()
