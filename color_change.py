import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)

text = "Hello, World!"
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
color_index = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                color_index += 1

    screen.fill((0, 0, 0))

    for i, letter in enumerate(text):
        surface = font.render(letter, True, GREEN if i < color_index else BLUE)
        screen.blit(surface, (20 + i * 20, 100))

    pygame.display.flip()