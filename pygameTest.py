import pygame
import sys
import random
import time
import re

# Initialiser Pygame
pygame.init()

# Charger les mots depuis le fichier
def load_words(filename):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words

#Charger les mots depuis le fichier
words = load_words("words.txt")

# Configurer la fenêtre
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Couleurs
WHITE = (255, 255, 255)
BLUE_LIGHT = (38, 184, 190)

# Police
font = pygame.font.Font(None, 60)
small_font = pygame.font.Font(None, 30)

#Charger les images du pendu
hangman_images = []
for i in range(7):
    image = pygame.image.load(f"images/hangman{i}.png")
    image = pygame.transform.scale(image, (200, 200)) #Redimmentionner l'image
    hangman_images.append(image)

#Initialiser les scores 
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
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 150))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 200))
        screen.blit(new_word_text, (WIDTH // 2 - new_word_text.get_width() // 2, 250))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 300))
        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Touche P pour Play
                    return "play"
                elif event.key == pygame.K_s:  # Touche S pour Score_text
                    display_scores()
                elif event.key == pygame.K_w:  # Touche w pour New Word
                    return "new_word"
                elif event.key == pygame.K_q:  # Touche q pour Quit
                    return "quit"
                
def display_scores():
    while True:
        #fond blanc
        screen.fill(WHITE)

        #Texte des scores
        score_text = font.render(f"Score - Wins: {wins} Loses: {loses}", True, BLUE_LIGHT)
        back_text = font.render("Back to Menu[B]", True, BLUE_LIGHT)

        #Afficher les textes sur l'écran
        screen.blit(score_text, (WIDTH // 2 -score_text.get_width() // 2,  HEIGHT // 2 - 50))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        #Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: #Touche B pour retourner au menu
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
    prompt_text = font.render("Please enter your name:", True, BLUE_LIGHT) # Définir le texte de la demande
    message = ""
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si l'utilisateur clique sur la boîte d'entrée
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                        message =f" Hello {text}! Lest's play Hangman!"
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
        screen.fill(WHITE)
        # Afficher le texte de la demande
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
    """Demander un mot à l'utilisateur via une interface graphique Pygame."""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    message = "" #Initialiser la variable message
    

    # Définir le texte de la demande
    prompt_text = font.render("Please enter a word:", True, BLUE_LIGHT)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si l'utilisateur clique sur la boîte d'entrée
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
        # Afficher le texte de la demande
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

    # Affiche le message après que le mot ait été entré
    screen.fill(WHITE)
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 - 80))
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    message_surface =small_font.render(message, True, BLUE_LIGHT)
    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    time.sleep(3)


    return text
#Pour afficher les scores
   
#Afficher les images en fonction des erreurs

def display_hangman(errors):
    screen.blit(hangman_images[errors], (WIDTH // 2 - hangman_images[errors].get_width() // 2, 50)) 

def animate_message(message):
    font_large = pygame.font.Font(None, 100)   
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = 5, 5 #vitess de déplacement

    for _ in range(100): #Nombre de fois que le message se déplace
        screen.fill(WHITE) 
        text_surface = font_large.render(message, True, BLUE_LIGHT)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(50) #Délai de 50 millisecondes

        #Mettre à jour la position du texte
        x += dx
        y += dy

        # Inverser la direction si le texte atteint les bords de l'écran
        if text_rect.left <= 0 or text_rect.right >= WIDTH:
            dx = -dx
        if text_rect.top <= 0 or text_rect.bottom >= HEIGHT:
            dy = -dy       

#Définir les fonctions de jeu
def play_game(words): 
    global wins, loses
    word = random.choice(words).upper()
    guessed = ["_"] * len(word)
    guessed_letters = set()
    errors = 0

    while errors < len(hangman_images) - 1 and "_" in guessed:
        screen.fill(WHITE)
        display_hangman(errors)

        # Affiche le mot deviné j'usqu'à present
        guessed_word = " ".join(guessed)
        guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
        screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2 + 100))

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

    screen.fill(WHITE)      
    display_hangman(errors) 
    guessed_word =" ".join(guessed)
    guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
    screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    time.sleep(1)

     # Mettre à jour les scores et afficher les messages
    if "_" not in guessed:
        wins += 1
        message ="You're win!"
    else: 
        loses += 1
        message = "You're lose!"

     # Afficher le message animé de victoire ou de défaite
    animate_message(message)   

def play_game(words):
    global wins, loses
    word = random.choice(words).upper()
    guessed = ["_"] * len(word)
    guessed_letters = set()
    errors = 0

    while errors < len(hangman_images) - 1 and "_" in guessed:
        screen.fill(WHITE)
        display_hangman(errors)

        #Affiche le mot deviné jusqu'à présent
        guessed_word = " ".join(guessed)
        guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
        screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2 + 100))

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

    screen.fill(WHITE)      
    display_hangman(errors) 
    guessed_word =" ".join(guessed)
    guessed_word_surface = font.render(guessed_word, True, BLUE_LIGHT)
    screen.blit(guessed_word_surface, (WIDTH // 2 - guessed_word_surface.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    time.sleep(3)

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