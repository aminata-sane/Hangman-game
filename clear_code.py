import random
import pygame
import os
import sys

# Pygame initialisation 
pygame.init()

# Showing the interface
display_width = 800
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Hangman")

# main colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (100, 149, 237)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 36)

# Global variables
score_file = "scores.txt"
words_list = "words.txt"
player_name = ""
score = 0

# The button
def draw_button(x, y, width, height, text, default_color, hover_color, action = None, padding=5):
    # Draws a button with hover and click effects
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[0] < y + height:
        pygame.draw.rect(window, hover_color, (x, y, width, height))

        if click[0] == 1 and action is not None: 
            action()
        else:
            pygame.draw.rect(window, default_color(x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x+width//2, y+height//2))
    window.blit(text_surface, text_rect)
