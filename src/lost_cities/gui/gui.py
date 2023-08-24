import pygame
from pygame import Surface
from lost_cities.card import Card
from lost_cities.gui.utils import extract_card
from lost_cities.gui.settings import settings
import numpy as np

pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Lost Cities GUI")

board_image: Surface = pygame.image.load("src/lost_cities/gui/assets/board.webp")
print(board_image.get_width(), board_image.get_height())
# Position des tas, de la pioche et de la défausse


running = True
selected_card = None

back: np.ndarray = extract_card("Back", 0)
hand = [
    Card("Yellow", 7),
    Card("Blue", 0),
    Card("Red", 2),
    Card("White", 10),
    Card("Green", 6),
    Card("Red", 9),
    Card("Red", 0),
    Card("White", 0),
]
hand.sort()

all_green = [Card("Green", 0)] * 3 + [Card("Green", i) for i in range(2, 8)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        #     # Vérification si une carte en main est sélectionnée
        #     for card in hand:
        #         if card.rect.collidepoint(event.pos) and not card.played:
        #             selected_card = card

        #     # Vérification si la pioche est sélectionnée
        #     if deck_rect.collidepoint(event.pos):
        #         # Mettre en œuvre la logique de pioche ici
        #         pass

        #     # Vérification si la défausse est sélectionnée
        #     if discard_rect.collidepoint(event.pos):
        #         # Mettre en œuvre la logique de défausse ici
        #         pass

    screen.fill(settings.WHITE)

    # Dessin des cartes en main
    for i, card in enumerate(all_green):
        x, y = settings.pile_positions["player"][card.color]
        y += 20 * i
        screen.blit(pygame.pixelcopy.make_surface(np.flipud(np.rot90(card.img))), (x, y))

    for i, card in enumerate(all_green):
        x, y = settings.pile_positions["computer"][card.color]
        y -= 20 * i
        screen.blit(pygame.pixelcopy.make_surface(np.flipud(np.rot90(card.img))), (x, y))
    # Mettre en œuvre la logique de placement des cartes sur le plateau ici

    # deck
    screen.blit(pygame.pixelcopy.make_surface(np.flipud(back)), settings.deck_position)

    # discard
    screen.blit(pygame.pixelcopy.make_surface(np.flipud(Card("White", 0).img)), settings.discard_position)

    # hand
    font = pygame.font.Font("src/lost_cities/gui/assets/atlantis_font.ttf", 40)
    hand_text = font.render("Hand:", True, (200, 200, 200))
    screen.blit(hand_text, (5, 5))

    for i, card in enumerate(hand):
        x = 5
        y = 100 + settings.CARD_HEIGHT / 2 * i
        screen.blit(pygame.pixelcopy.make_surface(np.flipud(np.rot90(card.img))), (x, y))

    # board
    screen.blit(board_image, settings.board_position)
    pygame.display.flip()

pygame.quit()
