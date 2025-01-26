import pygame
import sys
import random
import time
import re

# Initialiser Pygame
pygame.init()

# Charger les mots depuis le fichier
def load_words(filename):
    """Charger les mots depuis un fichier et les retourner sous forme de liste."""
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words

# Charger les mots depuis le fichier
words = load_words("words.txt")

# Configurer la fenêtre
WIDTH, HEIGHT = 800, 600  # Augmenter la taille de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Couleurs
WHITE = (255, 255, 255)
BLUE_LIGHT = (38, 184, 190)

# Police
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 30)

# Charger et redimensionner les images du pendu
hangman_images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    image = pygame.transform.scale(image, (200, 200))  # Redimensionner l'image à 200x200 pixels
    hangman_images.append(image)

# Initialiser les scores
wins = 0
loses = 0

def display_menu():
    """Afficher le menu et renvoyer le choix du joueur."""
    while True:
        # Fond blanc
        screen.fill(WHITE)

        # Textes du menu
        title_text = font.render("Hangman-Game", True, BLUE_LIGHT)
        play_text = font.render("Play [P]", True, BLUE_LIGHT)
        score_text = font.render("Score [S]", True, BLUE_LIGHT)
        new_word_text = font.render("A new word ? [W]", True, BLUE_LIGHT)
        quit_text = font.render("Quit [Q]", True, BLUE_LIGHT)

        # Afficher les textes sur l'écran
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 200))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(new_word_text, (WIDTH // 2 - new_word_text.get_width() // 2, 400))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 500))
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Touche P pour Play
                    return "play"
                elif event.key == pygame.K_s:  # Touche S pour Score
                    display_scores()
                elif event.key == pygame.K_w:  # Touche W pour New Word
                    return "new_word"
                elif event.key == pygame.K_q:  # Touche Q pour Quit
                    return "quit"

def display_scores():
    """Afficher les scores."""
    while True:
        # Fond blanc
        screen.fill(WHITE)

        # Textes des scores
        score_text = font.render(f"Score - Wins: {wins} Loses: {loses}", True, BLUE_LIGHT)
        back_text = font.render("Back to Menu [B]", True, BLUE_LIGHT)

        # Afficher les textes sur l'écran
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Touche B pour retourner au menu
                    return

def user_name():
    """Demander le nom de l'utilisateur via une interface graphique Pygame."""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    prompt_text = font.render("Please enter your name:", True, BLUE_LIGHT)
    message = ""

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                        message = f"Hello, {text}. Time to play hangman!"
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        if message:
            message_surface = small_font.render(message, True, BLUE_LIGHT)
            screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

    # Attendre que l'utilisateur appuie sur une touche pour continuer
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

    return text

def user_word():
    """Demander un mot à l'utilisateur via une interface graphique Pygame et l'enregistrer dans le fichier words.txt."""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    message = ""  # Initialiser la variable message

    # Définir le texte de la demande
    prompt_text = font.render("Please enter a word:", True, BLUE_LIGHT)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                        # Enregistrer le mot dans le fichier words.txt
                        try:
                            with open("words.txt", "a") as file:
                                file.write(text + "\n")
                            message = f"The new word is '{text}'"
                        except IOError:
                            message = "Error: Could not write to file."
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        if message:
            message_surface = small_font.render(message, True, BLUE_LIGHT)
            screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

    # Afficher le message après que le mot a été ajouté
    screen.fill(WHITE)
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    message_surface = small_font.render(message, True, BLUE_LIGHT)
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    time.sleep(3)  # Attendre 3 secondes avant de retourner au menu

    return text

def display_hangman(errors):
    """Afficher l'image du pendu en fonction du nombre d'erreurs."""
    screen.blit(hangman_images[errors], (WIDTH // 2 - hangman_images[errors].get_width() // 2, 50))

def animate_message(message):
    """Afficher un message animé et en mouvement."""
    font_large = pygame.font.Font(None, 100)
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 5, 5  # Vitesse de déplacement

    for _ in range(100):  # Nombre de frames pour l'animation
        screen.fill(WHITE)
        text_surface = font_large.render(message, True, BLUE_LIGHT)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(50)  # Délai entre les frames

        # Mettre à jour la position
        x += dx
        y += dy

        # Inverser la direction si le texte atteint les bords de l'écran
        if text_rect.left <= 0 or text_rect.right >= WIDTH:
            dx = -dx
        if text_rect.top <= 0 or text_rect.bottom >= HEIGHT:
            dy = -dy

def display_virtual_keyboard():
    """Afficher un clavier virtuel en dessous de la zone des mots du jeu."""
    keys = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    key_width = 40
    key_height = 40
    margin = 5
    start_x = (WIDTH - (key_width + margin) * 13) // 2
    start_y = HEIGHT - 100  # Placer le clavier plus bas sur l'écran

    key_rects = []  # Liste pour stocker les rectangles des touches

    for i, key in enumerate(keys):
        x = start_x + (i % 13) * (key_width + margin)
        y = start_y + (i // 13) * (key_height + margin)
        rect = pygame.Rect(x, y, key_width, key_height)
        key_rects.append((rect, key))
        pygame.draw.rect(screen, BLUE_LIGHT, rect)
        key_surface = font.render(key, True, WHITE)
        screen.blit(key_surface, (x + (key_width - key_surface.get_width()) // 2, y + (key_height - key_surface.get_height()) // 2))

    return key_rects

def play_game(words):
    """Jouer au jeu du pendu."""
    global wins, loses  # Utiliser les variables globales pour les scores
    word = random.choice(words).upper()
    guessed = ["_"] * len(word)
    guessed_letters = set()
    errors = 0

    while errors < len(hangman_images) - 1 and "_" in guessed:
        screen.fill(WHITE)
        display_hangman(errors)

        # Afficher le mot deviné jusqu'à présent
        guessed_word = " ".join(guessed)
        guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
        screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2))

        # Afficher le clavier virtuel et obtenir les rectangles des touches
        key_rects = display_virtual_keyboard()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                letter = event.unicode.upper()
                if letter.isalpha() and letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter in word:
                        for i, char in enumerate(word):
                            if char == letter:
                                guessed[i] = letter
                    else:
                        errors += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, key in key_rects:
                    if rect.collidepoint(mouse_pos):
                        letter = key
                        if letter not in guessed_letters:
                            guessed_letters.add(letter)
                            if letter in word:
                                for i, char in enumerate(word):
                                    if char == letter:
                                        guessed[i] = letter
                            else:
                                errors += 1

    screen.fill(WHITE)
    display_hangman(errors)
    guessed_word = " ".join(guessed)
    guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
    screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(1)

    # Mettre à jour les scores et afficher les messages
    if "_" not in guessed:
        wins += 1
        message = "You're win!"
    else:
        loses += 1
        message = "You're lose!"

    # Afficher le message animé de victoire ou de défaite
    animate_message(message)

# Exécuter le menu
running = True
while running:
    choice = display_menu()
    if choice == "play":
        print("Player chose to play.")
        name = user_name()
        print(f"Hello, {name}. Time to play hangman!")
        # Lancer le jeu directement avec les mots chargés depuis le fichier
        play_game(words)
    elif choice == "new_word":
        print("Player chose to enter a new word.")
        word = user_word()
        print(f"The new word is {word}.")
    elif choice == "quit":
        print("Player chose to quit.")
        running = False

pygame.quit()
sys.exit()