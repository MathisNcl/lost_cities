import pygame
from pygame import Surface
from lost_cities.card import Card
import numpy as np

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lost Cities GUI")

board_image: Surface = pygame.image.load("src/lost_cities/gui/assets/board.webp")

# Position des tas, de la pioche et de la défausse
pile_positions = {"Yellow": (140, 300), "Blue": (260, 300), "White": (380, 300), "Green": (505, 300), "Red": (630, 300)}
deck_position = (600, 300)
discard_position = (700, 300)


# Boucle principale du jeu
running = True
selected_card = None

hand = [Card("Yellow", 7), Card("Blue", 0), Card("Red", 2), Card("White", 10), Card("Green", 6)]

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

    # Dessin du plateau
    screen.fill(WHITE)
    screen.blit(board_image, (100, 100))

    # Dessin des cartes en main
    for card in hand:
        screen.blit(pygame.pixelcopy.make_surface(np.flipud(np.rot90(card.img))), pile_positions[card.color])

    # Mettre en œuvre la logique de placement des cartes sur le plateau ici

    # Mise à jour de l'affichage
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
