import random
import pygame
import sys

# Pygame initialisation
pygame.init()

# Show the window of the game
display_width = 800
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Main menu")

# main colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
HIGHLIGHT = (100, 149, 237)

font = pygame.font.Font(None, 36)

# Button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(window, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, default_color, (x, y, width, height))

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    window.blit(text_surface, text_rect)

running = True
while running:
    window.fill(WHITE)

    # Corrected button positions (using numbers for coordinates)
    draw_button(300, 250, 200, 50, "Choose the level", GRAY, HIGHLIGHT)
    draw_button(300, 320, 200, 50, "Play", GRAY, HIGHLIGHT)
    draw_button(300, 390, 200, 50, "Add new word", GRAY, HIGHLIGHT)
    draw_button(300, 460, 200, 50, "Watch score", GRAY, HIGHLIGHT)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# 1. Enter the user's name
username = ""
def name():
    pass

# 2. Main menu
def main_menu():
    pass

# 3. Menu for choosing the level
def level():
    pass

# 4. Menu for starting the game
def new_game():
    pass

# 5. Menu for adding the word
def add_word():
    pass

# 6. Menu for watching the scores
def open_score():
    pass

# 7. New name
def new_name():
    pass

if __name__ == "__main__":
    main_menu()


