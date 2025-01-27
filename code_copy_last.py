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

# Main colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#-------------------------------------- Game variables
difficulty_attempts = {"Light": 10, "Middle": 7, "Hard": 5}
selected_level = "Light"

# Add the words ---
def load_words():
    with open("words.txt", "r", encoding="utf-8") as file:
        words = file.readlines()
    return [word.strip() for word in words]

# Choose the word ---
def choose_word(words):
    return random.choice(words)

#  Main menu ---
def main_menu():
    running = True
    while running:
        window.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Main menu:", True, BLACK)
        option1 = font.render("1. Choose the level", True, BLACK)
        option2 = font.render("2. Start the game", True, BLACK)
        option3 = font.render("3. Add new word to the list", True, BLACK)
        option4 = font.render("4. Open the scores", True, BLACK)
        option5 = font.render("5. Exit", True, BLACK)

        # To show the text 
        window.blit(text, (50, 50))
        window.blit(option1, (50, 100))
        window.blit(option2, (50, 150))
        window.blit(option3, (50, 200))
        window.blit(option4, (50, 250))
        window.blit(option5, (50, 300))

        pygame.display.update()  

# ------------------------------------close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_x, mouse_y = event.pos
                if 50 < mouse_x < 400:
                    if 100 < mouse_y < 130:
                        # menu of choosing level
                        level_menu() 
                    elif 150 < mouse_y < 180:
                        # menu for starting game
                        start_game()  
                    elif 200 < mouse_y < 230:
                        # menu for adding word
                        add_word()  
                    elif 250 < mouse_y < 280:
                        # menu for watching the score
                        score_list()  
                    elif 300 < mouse_y < 330:
                        running = False  

# -------------------------------------- menu of choosing level ---
def level_menu():
    global selected_level
    running = True
    while running:
        window.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Choose level:", True, BLACK)
        option1 = font.render("1. Light level", True, BLACK)
        option2 = font.render("2. Middle level", True, BLACK)
        option3 = font.render("3. Hard level", True, BLACK)
        option0 = font.render("0. Go back", True, BLACK)


        window.blit(text, (50, 50))
        window.blit(option1, (50, 100))
        window.blit(option2, (50, 150))
        window.blit(option3, (50, 200))
        window.blit(option0, (50, 250))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 50 < mouse_x < 400:
                    if 100 < mouse_y < 130:
                        selected_level = "Light"
                        print("Light level selected")
                        running = False
                    elif 150 < mouse_y < 180:
                        selected_level = "Middle"
                        print("Middle level selected")
                        running = False
                    elif 200 < mouse_y < 230:
                        selected_level = "Hard"
                        print("Hard level selected")
                        running = False
                    elif 250 < mouse_y < 280:
                        # to go to the main menu
                        running = False

# 

# -----------------------------------------grafic of handman
def draw_hangman(screen, attempts_left):
    # Base for the gallows
    pygame.draw.line(screen, BLACK, (300, 500), (500, 500), 5)
    pygame.draw.line(screen, BLACK, (400, 500), (400, 150), 5)
    pygame.draw.line(screen, BLACK, (400, 150), (450, 150), 5)
    pygame.draw.line(screen, BLACK, (450, 150), (450, 200), 5)

    # Draw parts of the hangman based on remaining attempts
    if attempts_left <= 5:
        pygame.draw.circle(screen, BLACK, (450, 230), 30, 5)  # Head
    if attempts_left <= 4:
        pygame.draw.line(screen, BLACK, (450, 260), (450, 350), 5)  # Body
    if attempts_left <= 3:
        pygame.draw.line(screen, BLACK, (450, 270), (400, 320), 5)  # Left arm
    if attempts_left <= 2:
        pygame.draw.line(screen, BLACK, (450, 270), (500, 320), 5)  # Right arm
    if attempts_left <= 1:
        pygame.draw.line(screen, BLACK, (450, 350), (400, 430), 5)  # Left leg
    if attempts_left <= 0:
        pygame.draw.line(screen, BLACK, (450, 350), (500, 430), 5)  # Right leg

# ----------------------------------------- menu for starting game ---
def start_game():
    global selected_level
    words = load_words()
    word = choose_word(words).upper()
    guessed = ["_" for _ in word]
    guessed_letters = set()
    attempts_left = difficulty_attempts[selected_level]
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
            x = 50 + (i % 13) * 50
            y = 500 + (i // 13) * 50
            color = RED if letter in guessed_letters and letter not in word else GREEN if letter in guessed_letters else BLACK
            text = font_small.render(letter, True, color)
            window.blit(text, (x, y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                print('salut')
                if event.key >= pygame.K_a and event.key <= pygame.K_z:  
                    # Letter from kayboard
                    letter = chr(event.key).upper() 
                    if letter in alphabet and letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter in word:
                            for i, l in enumerate(word):
                                if l == letter:
                                    guessed[i] = letter
                        else:
                            attempts_left -= 1

        # -----------------------------Win/lost
        if "_" not in guessed:
            end_message("You Win!", GREEN)
            running = False

        if attempts_left == 0:
            end_message(f"You Lose! The word was {word}", RED)
            running = False

#--------------------------------------- Function to display end message
def end_message(message, color):
    window.fill(WHITE)
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(display_width // 2, display_height // 2))
    window.blit(text, (400 - text.get_width() // 2, 400 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

# ------------------------------------- menu for adding word ---
def add_word():
    new_word = input("Enter your new word: ").strip().upper()
    # If the word has just letters
    if new_word.isalpha(): 
        with open("words.txt", "a", encoding="utf-8") as file:
            file.write(new_word + "\n")
        print(f"Word '{new_word}' added successfully!")
    else:
        print("Invalid input. Please enter a valid word consisting only of letters.")

# ------------------------------------ menu for viewing the scores ---
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

#--------------------------------  Main loop to start the game
if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")
