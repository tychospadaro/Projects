#! python2

words = str(input('enter a string: '))
print words

"""
A simple Monte Carlo solver for Nim
http://en.wikipedia.org/wiki/Nim#The_21_game
"""

import random
# import codeskulptor
# codeskulptor.set_timeout(20)

MAX_REMOVE = 3
TRIALS = 10

def evaluate_position(num_items):
    """
    Monte Carlo evalation method for Nim
    """
    # list with win ratios of possible moves
    # number removed is index +1
    moves = [number for number in range(1, MAX_REMOVE + 1)]

    for move in moves:
        trial = 0
        wins = 0
        while trial < TRIALS:
            wins += run_trial(num_items, move)
            trial += 1
        move = float(wins/TRIALS)

    best = max(moves)

    return moves.index(best) + 1

def run_trial(num_items, move):
    '''
    given...
    num_items	- number of items remaining.
    move		- computer # of items removed.

    play randomly for remainder of game.
    return 1 on computer win, 0 on loss.
    '''
    remaining = num_items - move
    computer_just_played = True

    while remaining > 0:
        remaining -= random.randrange(1, MAX_REMOVE + 1)
        computer_just_played != computer_just_played

    if computer_just_played:
        return 1
    else:
        return 0

def play_game(start_items):
    """
    Play game of Nim against Monte Carlo bot
    """

    current_items = start_items
    print "Starting game with value", current_items
    while True:
        comp_move = evaluate_position(current_items)
        current_items -= comp_move
        print "Computer choose", comp_move, ", current value is", current_items
        if current_items <= 0:
            print "Computer wins"
            break
        player_move = int(input("Enter your current move"))
        current_items -= player_move
        print "Player choose", player_move, ", current value is", current_items
        if current_items <= 0:
            print "Player wins"
            break

play_game(9)
#play_game(21)
