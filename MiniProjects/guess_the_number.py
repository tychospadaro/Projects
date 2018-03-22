# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random, math

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

range_min, range_max = 0, 100
hints = False

# helper function to start and restart the game
def new_game():
    """starts a new game"""
    global secret_number, min_guess, max_guess, tries
    secret_number = random.randrange(range_min, range_max)
    min_guess, max_guess = range_min, range_max
    tries = max_tries()

    print ()
    print ('Beginning new game')
    print ('Guess the secret number between ' + str(range_min)
           + ' and ' + str(range_max-1) + '.')
    print ('You have ' + str(tries) + ' guesses')

def max_tries():
    """return the max tries based on range_min and range_max"""
    tries = 0
    while 2 ** tries < range_max - range_min + 1:
        tries += 1
    return tries

def optimal_guess(low, high):
    """return the average of the current high and low guess"""
    return str((low + high) // 2)

def change_range(new_min, new_max):
    """called by other functions to change the range"""
    global range_min, range_max
    if range_min == new_min and range_max == new_max:
        print ('Range already [' + str(range_min) + ',' + str(range_max) + ')...')
    else:
        print ('Changing range to [' + str(range_min) + ',' + str(range_max) + ')')
        range_min, range_max = new_min, new_max
    new_game()

# define event handlers for control panel
def range100():
    """handler to reset range to [0,100)"""
    change_range(0, 100)

def range1000():
    """handler to reset range to [0,1000)"""
    change_range(0, 1000)

def set_range(new_range):
    """handler to reset range to [user_min, user_max)"""
    clean_input = new_range.strip('[)')		# could add further validation/cleaning here
    user_min, user_max = clean_input.split(',')
    change_range(int(user_min), int(user_max))

def toggle_hints():
    """toggles printing of optimal play hints"""
    global hints
    if hints:
        print ('Turning off hints')
    else:
        print ('Turning on hints')
        print ("Optimal guess: " + optimal_guess(min_guess, max_guess))
    hints = not hints

def input_guess(guess):
    """accepts user input guess and outputs depending on high/low/correct answer"""
    print ()
    global tries
    tries -= 1
    if tries <= 0:
        print ('Last chance!')

    print ("Guess was " + guess)
    int_guess = int(guess)

    if int_guess > secret_number: 	# guess too big
        print ("Lower")
        global max_guess		    # update current max
        max_guess = int_guess
    elif int_guess < secret_number: # guess too low
        print ("Higher")
        global min_guess				# update current min
        min_guess = int_guess
    else:
        print ("Correct")
        print ('Resetting at current range: [' + str(range_min) + ',' + str(range_max) + ')')
        new_game()

    if tries <= 0:
        print ('You lost!')
        print ('Resetting at current range: [' + str(range_min) + ',' + str(range_max) + ')')
        new_game()
    elif tries < max_tries():
        print ('You have ' + str(tries) + ' guesses remaining')

    if hints:
        print ("Optimal next guess: " + optimal_guess(min_guess, max_guess))

# create frame
frame = simplegui.create_frame('Guess the number', 200, 500)

# register event handlers for control elements and start frame
frame.add_input('Enter guess', input_guess, 50)
frame.add_label('',100)
frame.add_label('WARNING:',50)
frame.add_label('Any attempts to "Change Range" will reset the current game.',120)
frame.add_button('Change Range to [0,100)', range100, 110)
frame.add_button('Change Range to [0,1000)', range1000, 110)
frame.add_label('',100)
frame.add_label('Extras:',100)
frame.add_button('Reset Game (Same Range)', new_game, 110)
frame.add_label('Change Range to',150)
frame.add_input('[user_min, user_max)', input_guess, 50)
frame.add_button('Hints?', toggle_hints, 110)

# call new_game
new_game()

frame.start()

# always remember to check your completed program against the grading rubric
