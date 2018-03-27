# implementation of card game - Memory

import random
from math import pi

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


deck = [_dum for _dum in range(8)] 	\
      + [_dum for _dum in range(8)]		# create cards from 0-7 twice
CARD_W = 50
CARD_H = 100
ROTATE = float(pi/2)
turn = 0
cool_cards = False

# Note: the flag of Nepal is awesome and shall not be rotated. (card_1)
card_0 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/commons/e/ef/International_Flag_of_Planet_Earth.svg')
card_1 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg')
card_2 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Kenya.svg')
card_3 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/en/4/4c/Flag_of_Sweden.svg')
card_4 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg')
card_5 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg')
card_6 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/commons/3/38/NZ_flag_design_Silver_Fern_%28Black%2C_White_%26_Blue%29_by_Kyle_Lockwood.svg')
card_7 = simplegui.load_image('https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Antarctica_%28Smith%29.svg')

flag_cards = [card_0, card_1, card_2, card_3, card_4, card_5, card_6, card_7]

# helper function to initialize globals
def new_game():
    global covered, first_flip, selected, turn
    covered = [True for _dum in range(16)]	# cover all cards
    first_flip = None					# reset game state
    selected = [None, None]				# reset selected cards
    turn = 0							# reset turn counter
    random.shuffle(deck) 				# shuffle deck

def poly(card_num):						# return card cover coords
    bottom, top = CARD_H, 0
    left, right = card_num * CARD_W, (card_num + 1) * CARD_W
    return [(left,bottom),(left,top),(right,top),(right,bottom)]

def switch_cards():						# toggle flag cards
    global cool_cards

    for idx, flag in enumerate(flag_cards):
        if type(flag) is list:			# image already converted
            continue
        if flag.get_width() > 0:		# image is loaded, convert image
            flag_cards[idx] = argify(flag)	# into draw_image([args...])

    if not all(type(flag) is list for flag in flag_cards):
        text_box.set_text("Not all images have loaded. Please try again shortly.")
        return

    if not cool_cards:					# turn on cool_cards flag
        cool_cards = True
    else:								# turn off cool_cards flag
        text_box.set_text('aww, sad panda')			# lame.
        cool_cards = False


def argify(image):						# take in simplegui 'Image'
    src_width = image.get_width()		# return as args for
    src_height = image.get_height()		# simplegui canvas.draw_image()
    src_cen = [src_width // 2, src_height // 2]
    src_w_h = [src_width, src_height]
    dst_cen = [0 , CARD_H // 2]			# center x pos set in draw handler
    dst_w_h = [CARD_H, CARD_W]			# swap W & H due to rotation
    rot = ROTATE
    if src_w_h == [726, 885]:			# w_h for flag of Nepal, too cool to rotate
        dst_w_h = [CARD_W, CARD_H]
        rot = 0
    return [image, src_cen, src_w_h, dst_cen, dst_w_h, rot]

# define event handlers
def mouseclick(pos):
    global first_flip, turn
    card_idx = pos[0] // 50				# find card index

    if covered[card_idx]:				# if covered
        covered[card_idx] = False		# reveal card
    else:								# else, exposed
        text_box.set_text('Card already revealed')	# print msg to console
        return							# exit handler

    if first_flip != True:				# if state was not first flip,
        first_flip = True				# then this is the first flip
    else:								# if it was,
        first_flip = False				# then this is the second flip

    if first_flip:					# on first flip
        if selected[0] != None:			# if cards selected
            covered[selected[0]] = True	# (i.e. not initial flip/match)
            covered[selected[1]] = True	# re-cover last guesses
        selected[0] = card_idx			# store first card index
        match = False					# no match on first flip
        turn += 1						# increment turn
        label.set_text("Turns = " + str(turn))	# update label
    else:							# on second flip
        selected[1] = card_idx			# store second card index
        match = deck[selected[0]] == deck[selected[1]]	# check match

    if match:							# if match
        selected[0], selected[1] = None, None	# de-select cards

# cards are logically 50x100 pixels in size
def draw(canvas):
    for idx, element in enumerate(deck):	# draw each card
        if cool_cards:						# use cool cards
            card_x_center = CARD_W * idx + CARD_W // 2
            flag_cards[element][3][0] = card_x_center
            canvas.draw_image(*flag_cards[element])
        else:								# use raw numbers
            canvas.draw_text(str(element), (CARD_W * idx + 15, 65), 42, 'Red')
        if covered[idx]:			# draw card cover
            canvas.draw_polygon(poly(idx), 1, 'Black', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
frame.add_button('Card Style', switch_cards)
label = frame.add_label("Turns = 0")
text_box = frame.add_label('')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
