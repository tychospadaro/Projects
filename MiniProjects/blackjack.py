# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

PAD = 20

# initialize some useful global variables
in_play = False
cheat_flag = False
dealer_card = ''
next_card = ''
dealer_val = ''
player_val = ''
outcome = ""
next_action = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, \
            [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def __str__(self):
        str_out = self.name + "'s hand contains "
        for card in self.cards:
            str_out += str(card) + ' '
        str_out += '. Value is ' + str(self.get_value()) + '.'
        return str_out

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = 0
        aces = False
        for card in self.cards:
            rank = card.get_rank()
            total += VALUES[rank]
            if rank == 'A':
                aces = True

        if aces and total <= 11:
            total += 10

        return total

    def draw(self, canvas, pos):
        for idx, card in enumerate(self.cards):
            if idx == 0 and self.name == 'Dealer' and in_play:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, \
            [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1] + PAD], CARD_SIZE)
            else:
                corner_pos = (pos[0] + (PAD + CARD_SIZE[0])*idx, pos[1] + PAD)
                card.draw(canvas, corner_pos)

# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) \
                      for suit in SUITS \
                      for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)

    def cards_left(self):
        return str(len(self.cards)) + ' cards left in deck'

    def __str__(self):
        str_out = 'Deck contains '
        for card in self.cards:
            str_out += str(card) + ' '
        return str_out

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, p_hand, d_hand, hands, score, next_action
    outcome = ''
    if in_play:
        score -= 1
        outcome = 'You forfeit the hand.'

    deck = Deck()
    p_hand = Hand('Player')
    d_hand = Hand('Dealer')
    hands = [d_hand, p_hand]
    num_cards = 2

    for _round in range(num_cards):
        for player in hands:
            player.add_card(deck.deal_card())

#    for player in hands:
#        print player

    in_play = True
    next_action = 'Hit or stand?'

def hit():
    global score, in_play, outcome, next_action
    if not in_play:
        outcome = 'You are not currently playing.'
        next_action = 'New deal?'
        return
    else:
        p_hand.add_card(deck.deal_card())
        outcome = ''
        next_action = 'Hit or stand?'

    if p_hand.get_value() > 21:
        score -= 1
        outcome = 'You have busted!'
        next_action = 'New deal?'
        in_play = False

def stand():
    global score, in_play, outcome, next_action
    if not in_play:
        outcome = 'You are not currently playing.'
        next_action = 'New deal?'
        return

    while d_hand.get_value() < 17:
        d_hand.add_card(deck.deal_card())

    if d_hand.get_value() > 21:
        score += 1
        outcome = 'Dealer busted!'
    elif d_hand.get_value() < p_hand.get_value():
        score += 1
        outcome = 'You beat the dealer!'
    else:
        score -= 1
        outcome = 'You lost to the dealer!'
    next_action = 'New deal?'
    in_play = False

def cheat_flag_handler():
    global cheat_flag
    cheat_flag = not cheat_flag
    print cheat_flag

def cheat_update():
    global dealer_card, next_card, dealer_val, player_val
    if cheat_flag:
        dealer_card = d_hand.cards[0].get_rank()
        dealer_val = d_hand.get_value()
        next_card = 'Next card is a ' + deck.cards[0].get_rank()
    else:
        dealer_card = ''
        dealer_val = 'hidden'
        next_card = ''
    player_val = p_hand.get_value()

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('Blackjack', (20, 42), 42, 'Maroon')
    canvas.draw_text('Score ' + str(score), (480, 42), 32, 'Black')
    canvas.draw_text(d_hand.name , (60, 100), 32, 'Black')
    canvas.draw_text(p_hand.name , (60, 325), 32, 'Black')
    canvas.draw_text(outcome, (180, 100), 32, 'Black')
    canvas.draw_text(next_action, (180, 325), 32, 'Black')

    d_hand.draw(canvas, [60, 100])
    p_hand.draw(canvas, [60, 325])

    cheat_update()
    canvas.draw_text(str(dealer_card), (80, 280), 32, 'Black')
    canvas.draw_text(str(next_card) , (80, 505), 32, 'Black')
    canvas.draw_text('Total: ' + str(dealer_val) , (80, 250), 32, 'Black')
    canvas.draw_text('Total: ' + str(player_val) , (80, 475), 32, 'Black')


#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label('')
frame.add_button('Cheat', cheat_flag_handler, 200)

frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
