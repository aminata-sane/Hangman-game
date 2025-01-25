import random

HANGMAN_PICS = ['''
+---+
    |
    |
    |
=====''', '''
+---+
 O  |
    |
    |
=====''', '''
+---+
 O  |
 |  |
    |
=====''', '''
+---+
 O  |
/|  |
    |
=====''', '''
+---+
 O  |
/|\ |
    |
=====''', '''
+---+
 O  |
/|\ |
/   |
=====''', '''
+---+
 O  |
/|\ |
/ \ |
===== ''']

# List of words
words = 'python hangman computer keyboard puzzle monitor function variable algorithm developer program integer syntax runtime compile'.split()

def get_random_word(word_list):
    # Returns a random string from the passed list of strings.
    word_index = random.randint(0, len(word_list) - 1)
    return word_list[word_index]

def display_board(missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secret_word)
    for i in range(len(secret_word)):  # Replace blanks with correctly guessed letters.
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i + 1:]

    for letter in blanks:  # Show the secret word with spaces in between each letter.
        print(letter, end=' ')
    print()

def get_guess(already_guessed):
    # Ensures the player enters a single valid letter.
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

def play_again():
    # Asks the player if they want to play again.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Game logic
print('H A N G M A N')
missed_letters = ''
correct_letters = ''
secret_word = get_random_word(words)
game_is_done = False

while True:
    display_board(missed_letters, correct_letters, secret_word)
    guess = get_guess(missed_letters + correct_letters)

    if guess in secret_word:
        correct_letters += guess

        # Check if the player has won.
        found_all_letters = True
        for i in range(len(secret_word)):
            if secret_word[i] not in correct_letters:
                found_all_letters = False
                break
        if found_all_letters:
            print(f'Yes! The secret word is "{secret_word}"! You have won!')
            game_is_done = True
    else:
        missed_letters += guess

        # Check if the player has lost.
        if len(missed_letters) == len(HANGMAN_PICS) - 1:
            display_board(missed_letters, correct_letters, secret_word)
            print(f'You have run out of guesses!\nAfter {len(missed_letters)} missed guesses and {len(correct_letters)} correct guesses, the word was "{secret_word}".')
            game_is_done = True

    # Ask if the player wants to play again.
    if game_is_done:
        if play_again():
            missed_letters = ''
            correct_letters = ''
            game_is_done = False
            secret_word = get_random_word(words)
        else:
            break
