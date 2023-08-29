from typing import Any, Optional

import numpy as np
import pygame
from pygame import Rect, Surface

from lost_cities.card import Card
from lost_cities.game import LostCitiesGame
from lost_cities.gui.settings import settings
from lost_cities.gui.utils import extract_card


class GUIGame:
    def __init__(self) -> None:
        self.assets: dict[str, Surface] = {
            "board_image": pygame.image.load("src/lost_cities/gui/assets/board.webp"),
            "play_logo": pygame.image.load("src/lost_cities/gui/assets/play.png"),
            "discard_logo": pygame.image.load("src/lost_cities/gui/assets/trash.png"),
        }
        self.assets["deck"] = pygame.pixelcopy.make_surface(np.flipud(extract_card("Back", 0)))

        self.pygame_objects: dict[str, Rect] = {
            "play_logo_rect": self.assets["play_logo"].get_rect(),
            "discard_logo_rect": self.assets["discard_logo"].get_rect(),
            "deck_rect": self.assets["deck"].get_rect(),
        }

        # Update coord
        self.pygame_objects["play_logo_rect"].topleft = settings.logo_play_position  # type: ignore
        self.pygame_objects["discard_logo_rect"].topleft = settings.discard_play_position  # type: ignore
        self.pygame_objects["deck_rect"].topleft = settings.deck_position  # type: ignore

        # Pygame structure
        pygame.init()
        self.screen: Surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Lost Cities GUI")
        self.font = pygame.font.Font("src/lost_cities/gui/assets/atlantis_font.ttf", 40)
        self.hand_text = self.font.render("Hand:", True, (200, 200, 200))
        self.running: bool = True
        self.rect_selected: Optional[pygame.Rect] = None
        self.selected_card: Optional[Card] = None

        # Final Game
        self.game: LostCitiesGame = LostCitiesGame("Player1", "Computer", True)

    def show_setup_structure(self) -> None:
        """Blits important infos as:
        - Deck
        - Discard if there is one
        - Play and discard logo
        - Hand text
        """
        self.screen.fill(settings.WHITE)

        self.screen.blit(self.assets["deck"], settings.deck_position)
        self.screen.blit(self.font.render(f"{len(self.game.deck)}", True, settings.WHITE), settings.deck_text_position)

        # discard
        if self.game.discard_piles:
            self.screen.blit(self.game.discard_piles[-1].surface, settings.discard_position)

        # logo:
        self.screen.blit(self.assets["play_logo"], settings.logo_play_position)
        self.screen.blit(self.assets["discard_logo"], settings.discard_play_position)

        # hand
        self.screen.blit(self.hand_text, (5, 5))

    def show_played_cards(self) -> None:
        """Blits all cards played by both player in the board"""
        played_card = {"player": self.game.players[0].board, "computer": self.game.players[1].board}
        for player_side, colors in played_card.items():
            step: int = -20 if player_side == "computer" else 20
            for color, cards in colors.items():
                for i, card in enumerate(cards):
                    x, y = settings.pile_positions[player_side][color]
                    y += step * i
                    self.screen.blit(card.surface, (x, y))

    def show_hand(self) -> None:
        """Blits all player's cards and the rect for the selected one"""
        for i, card in enumerate(self.game.players[0].hand):
            x = 5
            y = 50 + settings.CARD_HEIGHT * 0.66 * i
            card.set_coord(x, y)
            self.screen.blit(card.surface, (x, y))

        if self.rect_selected is not None:
            pygame.draw.rect(self.screen, settings.RED, self.rect_selected, 2)

    def trigger_event(self) -> None:
        """Triggers all events based on a click"""
        if len(self.game.deck) == 0:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.game.current_player == 1 and len(self.game.deck) >= 1:
                self.game.play_round()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.choose_card(event)

                self.gui_action(event)

                self.pick_card_on_pile(event)

    def choose_card(self, event: pygame.event.Event) -> None:
        """Hightlight the selected card

        Args:
            event (pygame.event.Event): click event
        """
        for card in self.game.players[0].hand:
            if card.rect.collidepoint(event.pos):
                self.rect_selected = pygame.Rect(card.x, card.y, settings.CARD_WIDTH, settings.CARD_HEIGHT)
                self.selected_card = card

    def gui_action(self, event: pygame.event.Event) -> None:
        """Event action for playing and discard. Need to select a card before.

        Args:
            event (pygame.event.Event): click event
        """
        if self.selected_card is not None and self.pygame_objects["play_logo_rect"].collidepoint(event.pos):
            self.game.play_round(
                "play", str(self.game.players[0].hand.index(self.selected_card)), skip_card=True, gui=True
            )
            self.selected_card = None
            self.rect_selected = None

        elif self.selected_card is not None and self.pygame_objects["discard_logo_rect"].collidepoint(event.pos):
            x, y = settings.discard_position
            self.selected_card.set_coord(x, y)
            self.game.play_round("discard", str(self.game.players[0].hand.index(self.selected_card)), skip_card=True)
            self.selected_card = None
            self.rect_selected = None

    def pick_card_on_pile(self, event: pygame.event.Event) -> None:
        """Either take a card from discard or deck. Only trigger if you have less than 8 cards and there is a click on
        one the two piles.

        Args:
            event (pygame.event.Event): click event
        """
        if (
            len(self.game.players[0].hand) != 8
            and self.game.discard_piles
            and self.game.discard_piles[-1].rect.collidepoint(event.pos)
        ):
            self.game.discard_piles[-1].unrotate_surface_to_discard()
            self.game.pick_card("discard")
            self.game.switch_player()

        elif len(self.game.players[0].hand) != 8 and self.pygame_objects["deck_rect"].collidepoint(event.pos):
            self.game.pick_card("deck")
            self.game.switch_player()

    def stop_game(self) -> None:
        """End layout, display who wons into an ugly rectangle"""
        if len(self.game.deck) <= 0:
            pygame.draw.rect(
                self.screen, settings.BLACK, (settings.END_X, settings.END_Y, settings.END_WIDTH, settings.END_HEIGHT)
            )
            scores: dict[str, Any] = {player.name: player.compute_score() for player in self.game.players}
            game_ended_text: pygame.font.Font = self.font.render(  # type: ignore
                f"Winner: {max(scores, key=scores.get)}", True, settings.WHITE  # type: ignore
            )
            score_player1: pygame.font.Font = self.font.render(  # type: ignore
                f"Player1: {scores['Player1'][0]}", True, settings.WHITE
            )
            score_computer: pygame.font.Font = self.font.render(  # type: ignore
                f"Computer: {scores['Computer'][0]}", True, settings.WHITE
            )
            # mypy says bullshits
            self.screen.blit(
                game_ended_text,  # type: ignore
                ((settings.END_WIDTH - game_ended_text.get_width()) // 2, settings.END_Y + 50),  # type: ignore
            )
            self.screen.blit(
                score_player1,  # type: ignore
                ((settings.END_WIDTH - score_player1.get_width()) // 2, settings.END_Y + 150),  # type: ignore
            )
            self.screen.blit(
                score_computer,  # type: ignore
                ((settings.END_WIDTH - score_computer.get_width()) // 2, settings.END_Y + 250),  # type: ignore
            )

    def can_i_play(self, nb_testing: Optional[int] = None) -> None:
        """Launch the game

        Args:
            nb_testing (Optional[int]): If not None, stop the game at nb_testing loop index. Defaults to None.
        """

        self.game.setup()
        cpt: int = 0
        while self.running:
            self.show_setup_structure()
            self.show_played_cards()
            self.show_hand()
            self.trigger_event()
            self.screen.blit(self.assets["board_image"], settings.board_position)
            self.stop_game()
            pygame.display.flip()
            if nb_testing is not None and nb_testing >= cpt:
                break
            cpt += 1
        pygame.quit()


def main() -> None:  # pragma: nocover
    gameGUI = GUIGame()
    gameGUI.can_i_play()


if __name__ == "__main__":  # pragma: nocover
    main()
