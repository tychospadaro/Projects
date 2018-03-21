# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# helper functions

def name_to_number(name):
    """Input: name of hand 'thrown'
       Output: return number used by the program to represent a given'hand'"""

    if name == "rock": return 0
    elif name == "Spock": return 1
    elif name == "paper": return 2
    elif name == "lizard": return 3
    elif name == "scissors": return 4
    else: print "Error - Invalid input: " + name

def number_to_name(number):
    """Input: number representing a hand 'thrown'
       Output: return the name of given 'hand' as a string"""

    if number == 0: return "rock"
    elif number == 1: return "Spock"
    elif number == 2: return "paper"
    elif number == 3: return "lizard"
    elif number == 4: return "scissors"
    else: print "Error - Invalid number: " + number


def rpsls(player_choice):
    """Input: player's choice as a string
       Output: randomly generate computer choice,
        determine the winner,
        and print out results to consol. Return nothing."""

    print 											# blank line for game separation
    print "Player chooses " + player_choice			# print player choice

    player_number = name_to_number(player_choice)	# get player choice number
    comp_number = random.randrange(0,5)				# generate computer choice number
    comp_choice = number_to_name(comp_number)		# get computer choice as string

    print "Computer chooses " + comp_choice			# print computer choice

    # compute difference of comp_number and player_number modulo five
    # 0 = tie | 1,2 = player wins | 3,4 = computer wins
    # see link, tip #5, for mathematical reasoning
    # https://www.coursera.org/learn/interactive-python-1/supplement/NlFfP/code-clinic-tips

    diff_mod_5 = (player_number - comp_number) % 5	# determines result (see above)
    result = (diff_mod_5 + 1)//2					# converts results to 0, 1, or 2

    if result == 0: print "Player and computer tie!"# print tie message
    elif result == 1: print "Player wins!"			# print player win message
    elif result == 2: print "Computer wins!"		# print computer win message
    else: print "This is un-possible"				# this shouldn't happen...



# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
