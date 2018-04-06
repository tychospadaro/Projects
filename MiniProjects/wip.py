#! python
"""
Rock-paper-scissors-lizard-Spock
Python 3.6.4, Tkinter GUI
"""
import tkinter as tk
import random

WIDTH = 600
HEIGHT = 600
THROWN = ['rock', 'Spock', 'paper', 'lizard', 'scissors']
# helper functions
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createMenu()
        self.createButtons()
        self.createCanvas()

    def createMenu(self):
        top = self.winfo_toplevel()
        self.menuBar = tk.Menu(top)
        top['menu'] = self.menuBar

        self.subMenu = tk.Menu(self.menuBar)
        self.menuBar.add_cascade(label='Help', menu=self.subMenu)
        self.subMenu.add_command(label='About', command=self.__aboutHandler)

    def createButtons(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=0) #add row as bottom

    def createCanvas(self):
        self.canvas = tk.Canvas(self, width=WIDTH*0.8, bg='white')
        self.canvas.bg = '#000000'
        self.canvas.grid(column=1)

    def __aboutHandler(self):
        pass




def name_to_number(name):
    """Input: name of hand 'thrown'
       Output: return number used by the program to represent a given'hand'"""
    try:
        return THROWN.index(name)
    except ValueError:
        return f'Invalid input: {name}'

def number_to_name(number):
    """Input: number representing a hand 'thrown'
       Output: return the name of given 'hand' as a string
       Note: will not catch negative numbers in list range"""
    try:
        return THROWN[number]
    except IndexError:
        return f'Invalid number: {number}'

def rpsls(player_choice):
    """Input: player's choice as a string
       Output: randomly generate computer choice, determine the winner,
        and print out results to consol. Return nothing."""

    print ()											# blank line for game separation
    print ("Player chooses " + player_choice)			# print player choice

    player_number = name_to_number(player_choice)	# get player choice number
    comp_number = random.randrange(0,5)				# generate computer choice number
    comp_choice = number_to_name(comp_number)		# get computer choice as string

    print ("Computer chooses " + comp_choice)			# print computer choice

    # compute difference of comp_number and player_number modulo five
    # 0 = tie | 1,2 = player wins | 3,4 = computer wins
    # see link, tip #5, for mathematical reasoning
    # https://www.coursera.org/learn/interactive-python-1/supplement/NlFfP/code-clinic-tips

    diff_mod_5 = (player_number - comp_number) % 5	# determines result (see above)
    result = (diff_mod_5 + 1)//2					# converts results to 0, 1, or 2

    if result == 0: print ("Player and computer tie!")# print tie message
    elif result == 1: print ("Player wins!")			# print player win message
    elif result == 2: print ("Computer wins!")		# print computer win message
    else: print ("This is un-possible")				# this shouldn't happen...



# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

app = Application()
app.master.title('Rock, Paper, Scissors, Lizard, Spock')
app.mainloop()
