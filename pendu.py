import pygame
import os
import random
import json

# pygame setup
pygame.init()
width, height = 800, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")

# Button variables
Radius = 20
Gap = 15
letters = []
startx = round((width - (Radius * 2 + Gap) * 28 / 2))
starty = 400
A = 65
for i in range(26):
    x = startx + Gap * 2 + ((Radius * 2 + Gap) * (i % 13))
    y = starty + ((i // 13) * (Gap + Radius * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
letter_font = pygame.font.SysFont('comicsans', 25)
message_font = pygame.font.SysFont('comicsans', 50)

# Load images
IMAGE_FOLDER = "hangman-img"
images = [pygame.image.load(os.path.join(IMAGE_FOLDER, f"hangman{i}.png")) for i in range(7)]

# Game variables
hangman_status = 0
difficulty = "normal"  # Default difficulty: "normal" or "easy"
guessed_word = []
word_to_guess = ""
current_player = ""
scores = {}

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

# Function to load or save scores
def load_scores():
    global scores
    if os.path.exists("players.txt"):
        with open("players.txt", "r") as f:
            scores = json.load(f)
    else:
        scores = {}

def save_scores():
    with open("players.txt", "w") as f:
        json.dump(scores, f, indent=4)

# Function to load a random word from a text file
def get_random_word(file_path):
    with open(file_path, 'r') as f:
        words = f.read().splitlines()
    return random.choice(words)

# Function to reveal some letters for easy mode
def reveal_letters(word):
    revealed = list('_' * len(word))
    indices_to_reveal = random.sample(range(len(word)), max(1, len(word) // 8))  # Reveal ~50% of the letters
    for i in indices_to_reveal:
        revealed[i] = word[i]
    return revealed

# Function to reset game variables
def reset_game():
    global hangman_status, guessed_word, word_to_guess, letters
    hangman_status = 0
    word_to_guess = get_random_word('words.txt')
    if difficulty == "easy":
        guessed_word = reveal_letters(word_to_guess)
    else:
        guessed_word = ['_'] * len(word_to_guess)
    for letter in letters:
        letter[3] = True

# Function to display the word to guess
def draw_word():
    word_display = ' '.join(guessed_word)
    text = letter_font.render(word_display, 1, black)
    win.blit(text, (350, 200))

# Function to display a message
def display_message(message):
    win.fill(white)
    text = message_font.render(message, 1, black)
    win.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Function to handle adding a word to the file
def add_word():
    adding_word = True
    new_word = ""
    while adding_word:
        win.fill(white)
        prompt_text = message_font.render("Enter a word and press Enter:", 1, black)
        input_text = message_font.render(new_word, 1, black)
        win.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 50))
        win.blit(input_text, (width // 2 - input_text.get_width() // 2, height // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Add word when Enter is pressed
                    with open("words.txt", "a") as f:
                        f.write(new_word + "\n")
                    adding_word = False
                elif event.key == pygame.K_BACKSPACE:  # Remove the last character
                    new_word = new_word[:-1]
                elif event.unicode.isalpha():  # Add typed letter to the word
                    new_word += event.unicode

# Function to handle player login
def player_login():
    global current_player, scores
    choosing = True
    name_input = ""
    while choosing:
        win.fill(white)
        prompt_text = message_font.render("Enter your player name:", 1, black)
        input_text = message_font.render(name_input, 1, black)
        win.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 50))
        win.blit(input_text, (width // 2 - input_text.get_width() // 2, height // 2 + 10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_player = name_input
                    if current_player not in scores:
                        scores[current_player] = 0
                    choosing = False
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.unicode.isalnum():
                    name_input += event.unicode

# Function to show the start menu
def start_menu():
    global difficulty, run
    while True:
        win.fill(white)
        title_text = message_font.render("Welcome to Hangman!", 1, black)
        option1 = message_font.render("1: Add a word", 1, black)
        option2 = message_font.render("2: Play", 1, black)
        option3 = message_font.render("3: Choose difficulty", 1, black)
        player_text = message_font.render(f"Player: {current_player} | Score: {scores[current_player]}", 1, black)
        difficulty_text = message_font.render(f"Current difficulty: {difficulty}", 1, black)

        win.blit(title_text, (width // 2 - title_text.get_width() // 2, 50))
        win.blit(option1, (width // 2 - option1.get_width() // 2, height // 2 - 75))
        win.blit(option2, (width // 2 - option2.get_width() // 2, height // 2))
        win.blit(option3, (width // 2 - option3.get_width() // 2, height // 2 + 75))
        win.blit(player_text, (width // 2 - player_text.get_width() // 2, height - 390))
        win.blit(difficulty_text, (width // 2 - difficulty_text.get_width() // 2, height - 95))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                save_scores()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    add_word()
                elif event.key == pygame.K_2:
                    reset_game()
                    return
                elif event.key == pygame.K_3:
                    difficulty = "easy" if difficulty == "normal" else "normal"

# Function to handle guesses
def handle_guess(ltr):
    global hangman_status

    for letter in letters:
        if letter[2].lower() == ltr and letter[3]:
            letter[3] = False
            if ltr in word_to_guess.lower():
                for i, char in enumerate(word_to_guess):
                    if char.lower() == ltr:
                        guessed_word[i] = char
            else:
                hangman_status += 1
            break

# Function to ask for restarting the game or going back to menu
def ask_restart():
    global run
    while True:
        win.fill(white)
        prompt_text = message_font.render("Do you want to play again? (Y/N)", 1, black)
        win.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 - 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:  # Yes, restart the game
                    reset_game()
                    return
                elif event.key == pygame.K_n:  # No, go back to main menu
                    start_menu()
                    return

# Main game loop
load_scores()  # Load scores from file
player_login()  # Ask for player login
start_menu()  # Show the start menu first

while run:
    clock.tick(FPS)

    win.fill(white)
    draw_word()
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, black, (x, y), Radius, 3)
            text = letter_font.render(ltr, 1, black)
            win.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()

    if hangman_status == 6:  # Lost
        display_message("You lost!")
        scores[current_player] = max(0, scores[current_player] - 1)
        save_scores()
        ask_restart()  # Ask if they want to restart

    elif '_' not in guessed_word:  # Won
        display_message("You won!")
        scores[current_player] += 5
        save_scores()
        ask_restart()  # Ask if they want to restart

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            save_scores()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible and (x - Radius <= m_x <= x + Radius and y - Radius <= m_y <= y + Radius):
                    handle_guess(ltr.lower())
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                handle_guess(event.unicode.lower())

pygame.quit()
