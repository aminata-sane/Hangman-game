import pygame
import random
import sys
import os
# ----------------------------------------------Interface-----------------------
# Pygame initialisation 
pygame.init()

# Showing the interface
display_width = 800
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Main menu")

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
player_name = "Player"
selected_level = None
difficulty_attempts = {"Light": 10, "Middle": 7, "Hard": 5}
words_file = "words.txt"
score_file = "scores.txt"
score = 0
# ------------------------------Utility Functions-----------------------
# Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, padding=5):
    # Draws a button with hover and click effects
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

# Load words from a file
# Завантажуємо слова з файлу
def load_words(words_file):
    if not os.path.exists(words_file):
        with open(words_file, "w", encoding="utf-8") as file:
            # Default word if file doesn't exist
            file.write("example\n")

    with open(words_file, "r", encoding="utf-8") as file:
        content = file.read().strip()
    levels = content.split("\n\n")
    
    easy_words = levels[0].split("\n")  # Легкі слова
    medium_words = levels[1].split("\n")  # Середні слова
    hard_words = levels[2].split("\n") 
    return easy_words, medium_words, hard_words

def load_words_by_level():
    easy_words, medium_words, hard_words = load_words("words.txt")  # Потрібно вказати правильний шлях до файлу
    
    if selected_level == "Easy":
        return easy_words
    elif selected_level == "Medium":
        return medium_words
    elif selected_level == "Hard":
        return hard_words
    else:
        return []  # Якщо рівень не вибраний, повертаємо порожній список
    
# Choose words
def choose_word(words):
    return random.choice(words)

# Save scores to file
def save_score(name, score):
    with open(score_file, "a", encoding="utf-8") as file:
        file.write(f"{name}: {score}\n")

# ---------------------------------------Showing the menu-----------------------------------------------
def main_menu():
    global selected_level 
    running = True
    while running:
        window.fill(WHITE)

        # Corrected button positions (using numbers for coordinates)
        draw_button(300, 250, 200, 50, "The level", GRAY, HIGHLIGHT, level_menu)
        draw_button(300, 320, 200, 50, "Play", GRAY, HIGHLIGHT, start_game)
        draw_button(300, 390, 200, 50, "Add new word", GRAY, HIGHLIGHT, add_word)
        draw_button(300, 460, 200, 50, "Watch score", GRAY, HIGHLIGHT, score_list)
        draw_button(300, 530, 200, 50, "Exit", GRAY, HIGHLIGHT, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()


# ----------------------------------Enter Name-------------------------------------
def enter_name():
    global player_name
    running = True
    input_box = pygame.Rect(300, 400, 200, 50)
    color = GRAY
    text = ""

    while running:
        window.fill(WHITE)
        pygame.draw.rect(window, color, input_box)
        draw_button(300, 500, 200, 50, "Confirm", GRAY, HIGHLIGHT, lambda: set_name(text))
        draw_button(300, 570, 200, 50, "Back", GRAY, HIGHLIGHT, main_menu)

        text_surface = font.render(text, True, BLACK)
        window.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, text_surface.get_width() + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    set_name(text)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        pygame.display.update()

def set_name(name):
    global player_name
    player_name = name.strip() if name.strip() else "Player"
    print(f"Player name set to: {player_name}")
    save_score(player_name, 0)
    main_menu()

# ----------------------------------------------------Level----------------------------------
# function for choosing level
def level_menu():
    global selected_level
    running = True
    while running:
        window.fill(WHITE)
        draw_button(300, 200, 200, 50, "Easy", GRAY, HIGHLIGHT, lambda: set_level("Easy"))
        draw_button(300, 270, 200, 50, "Medium", GRAY, HIGHLIGHT, lambda: set_level("Medium"))
        draw_button(300, 340, 200, 50, "Hard", GRAY, HIGHLIGHT, lambda: set_level("Hard"))
        draw_button(300, 410, 200, 50, "Back", GRAY, HIGHLIGHT, main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Sets the selected level and returns to main menu.
def set_level(level):
    global selected_level
    selected_level = level
    print(f"Level selected: {selected_level}")
    # end_message(f"Level selected: {selected_level}", BLACK)
    # Перевіряємо чи вибрано правильний рівень
    if selected_level not in ["Easy", "Medium", "Hard"]:
        print("Error: Invalid level selected.")
        return
    # main_menu()
    start_game()
    

# ------------------------------Starting game------------------------------------------------------------------
# grafic of handman
def draw_hangman(screen, attempts_left):
    # Base for the gallows
    pygame.draw.line(screen, BLACK, (300, 500), (500, 500), 5)
    pygame.draw.line(screen, BLACK, (400, 500), (400, 150), 5)
    pygame.draw.line(screen, BLACK, (400, 150), (450, 150), 5)
    pygame.draw.line(screen, BLACK, (450, 150), (450, 200), 5)

    # Draw parts of the hangman based on remaining attempts
    if attempts_left <= 5:
        # head
        pygame.draw.circle(screen, BLACK, (450, 230), 30, 5)  
    if attempts_left <= 4:
        # body
        pygame.draw.line(screen, BLACK, (450, 260), (450, 350), 5) 
    if attempts_left <= 3:
        # left arm
        pygame.draw.line(screen, BLACK, (450, 270), (400, 320), 5)  
    if attempts_left <= 2:
        # right arm
        pygame.draw.line(screen, BLACK, (450, 270), (500, 320), 5)  
    if attempts_left <= 1:
        # left leg
        pygame.draw.line(screen, BLACK, (450, 350), (400, 430), 5)  
    if attempts_left <= 0:
        # right leg
        pygame.draw.line(screen, BLACK, (450, 350), (500, 430), 5)  

# Function for starting game
def start_game():
    global selected_level, player_name, score
    if selected_level is None:  # Якщо рівень не вибрано
        print("Error: Level not selected!")  # Повідомлення про помилку
        return  # Зупиняємо виконання функції, не починаємо гру
    
    # Якщо рівень вибрано, продовжуємо виконувати код для старту гри
    print(f"Starting game with level: {selected_level}")

    words = load_words_by_level()
    word = choose_word(words).upper()
    guessed = ["_" for _ in word]
    guessed_letters = set()
    attempts_left = 7
    score = 0
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    running = True
    while running:
        window.fill(WHITE)

        # Draw gallows and hangman
        draw_hangman(window, attempts_left)

        # Display the word
        font = pygame.font.Font(None, 72)
        display_word = " ".join(guessed)
        text_surface = font.render(display_word, True, BLACK)
        window.blit(text_surface, (400 - text_surface.get_width() // 2, 100))

        # Display alphabet
        font_small = pygame.font.Font(None, 36)
        for i, letter in enumerate(alphabet):
            x = 100 + (i % 9) * 70 
            y = 600 + (i // 9) * 50
            color = RED if letter in guessed_letters and letter not in word else GREEN if letter in guessed_letters else BLACK
            text = font_small.render(letter, True, color)
            window.blit(text, (x, y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key >= pygame.K_a and event.key <= pygame.K_z:  
                    # Letter from kayboard
                    letter = chr(event.key).upper() 
                    if letter  not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter in word:
                            for i, l in enumerate(word):
                                if l == letter:
                                    guessed[i] = letter
                        else:
                            attempts_left -= 1

        # -----------------------------Win/lost
        if "_" not in guessed:
            score += 1
            # print(f"Congratulations, {player_name}! You Win!", GREEN)
            end_message(f"Congratulations, {player_name}! You Win!", GREEN)
            return

        if attempts_left == 0:
            # print(f"Sorry, {player_name}. You Lose! The word was {word}", RED)
            end_message(f"Sorry, {player_name}. You Lose! The word was {word}", RED)
            save_score(player_name, score)
            return
#--------------------------------------- Function to display end message
def end_message(message, color):
    window.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render(message, True, color)
    window.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)
    main_menu()


# -----------------------------------------------------New word----------------------------------
# function for writing new word
def add_word():
    new_word = input("Enter your new word: ").strip().upper()
    # If the word has just letters
    if new_word.isalpha(): 
        with open("words.txt", "a", encoding="utf-8") as file:
            file.write(new_word + "\n")
        print(f"Word '{new_word}' added successfully!")
    else:
        print("Invalid input. Please enter a valid word consisting only of letters.")

# -------------------------------------------------------Scores-----------------------------------------
# function for saving the scores
def score_list():
    try:
        with open("scores.txt", "r", encoding="utf-8") as file:
            scores = file.readlines()
        if scores:
            print("Score list:")
            for score in scores:
                print(score.strip())
        else:
            print("No scores available.")
    except FileNotFoundError:
        print("Score file not found.")

# running = True

# ------------------------------------Quit Game----------------------------------
def quit_game():
    pygame.quit()
    sys.exit()
#--------------------------------  Main loop to start the game
if __name__ == "__main__":
    main_menu()
    # try:
    #     main_menu()
    # except Exception as e:
    #     print(f"An error occurred: {e}")

