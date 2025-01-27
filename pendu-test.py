import pygame
import os
import math
import random  # Added random module

# pygame setup
pygame.init()
width, height = 800, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")

# Button variables
Radius = 20
Gap = 15
letters = []
startx = round((width - ( Radius * 2  + Gap)* 28 / 2))
starty = 400
A = 65
B = 66
for i in range(26):
        x = startx + Gap * 2 + ((Radius * 2 + Gap)* (i % 13))
        y = starty + ((i // 13) * (Gap + Radius * 2))
        letters.append([x, y, chr(A + i), True])

# Fonts 
letter_font = pygame.font.SysFont('comicsans', 25)

# Load images
IMAGE_FOLDER = "hangman-img"  # Folder containing images
images = []

for i in range(7):  # Load 7 stages of the hangman
    image_path = os.path.join(IMAGE_FOLDER, f"hangman{i}.png")
    images.append(pygame.image.load(image_path))

# Game variables
hangman_status = 0

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Setup game loop
FPS = 60
clock = pygame.time.Clock()

# Function to load a random word from a text file
def get_random_word(file_path):
    with open(file_path, 'r') as f:
        words = f.read().splitlines()  # Read words line by line
    return random.choice(words)  # Choose a random word

# Function to add a word to the words.txt file
def add_word_to_file(file_path, word):
    with open(file_path, 'a') as f:
        f.write(f"{word}\n")  # Append the new word to the file

def draw_word():
    word_display = ' '.join(guessed_word)
    text = letter_font.render(word_display, 1, black)
    win.blit(text, (350, 200))
# Function to display the main menu
def draw_menu():
    win.fill(white)
    
    # Display menu options
    text_play = letter_font.render("Press 1 to Play or 2 to Add a Word", 1, black)
    win.blit(text_play, (200, 200))

    pygame.display.update()

# Function to display a prompt to enter a word
def draw_prompt(input_word):
    win.fill(white)

    text_prompt = letter_font.render("Enter a word to add:", 1, black)
    win.blit(text_prompt, (200, 200))

    # Display the word being typed by the player
    typed_word_display = letter_font.render(input_word, 1, black)
    win.blit(typed_word_display, (200, 250))

    pygame.display.update()

# Game loop for the main menu
def menu():
    run_menu = True
    while run_menu:
        draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start game
                    return "play"
                if event.key == pygame.K_2:  # Add word to file
                    return "add_word"

# Game loop for adding a word
def add_word():
    input_word = ""
    prompt = True
    while prompt:
        draw_prompt(input_word)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_word != "":  # Enter key
                    add_word_to_file('words.txt', input_word)  # Add the word to the file
                    prompt = False  # Exit loop
                elif event.key == pygame.K_BACKSPACE:
                    input_word = input_word[:-1]  # Remove last character
                else:
                    input_word += event.unicode  # Add character to word

# Main game loop
def game():
    global word_to_guess, guessed_word, hangman_status
    word_to_guess = get_random_word('words.txt')
    guessed_word = ['_'] * len(word_to_guess)  # List of guessed letters

    while True:
        clock.tick(FPS)
        win.fill(white)

        # Draw buttons
        for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(win, black, (x, y), Radius, 3)
                text = letter_font.render(ltr, 1, black)
                win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        win.blit(images[hangman_status], (150, 100))
        draw_word()  # Display the word to guess
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < Radius:
                            letter[3] = False  # Hide the letter
                            if ltr.lower() in word_to_guess.lower():
                                # Update guessed letters
                                for i, char in enumerate(word_to_guess):
                                    if char.lower() == ltr.lower():
                                        guessed_word[i] = char
                            else:
                                hangman_status += 1

# Main program
def main():
    while True:
        choice = menu()  # Display the menu
        if choice == "play":
            game()  # Start the game
        elif choice == "add_word":
            add_word()  # Add a word to the file

# Start the main program
main()
