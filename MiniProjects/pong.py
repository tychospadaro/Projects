# Implementation of classic arcade game Pong

import simplegui
import random

# Globals
# Base constants
WIDTH = 600
HEIGHT = 400

# Scalings
PAD_W_SCALE = 0.02		# 2% of width
PAD_H_SCALE = 0.20		# 20% of height
PAD_VEL_SCALE = 0.01 	# 1% of height per update
RADIUS_SCALE = 0.05		# 5% of height
BALL_VEL_SCALE = 1		# magic numbers in class, scale from here

# Derived constants
PAD_WIDTH = WIDTH * PAD_W_SCALE
PAD_HEIGHT = HEIGHT * PAD_H_SCALE
PAD_STOP = PAD_HEIGHT / 2
L_GUTTER = PAD_WIDTH
R_GUTTER = WIDTH - PAD_WIDTH
PADDLE_SPD = HEIGHT * PAD_VEL_SCALE
BALL_RADIUS = HEIGHT * RADIUS_SCALE

# Define classes
class Ball:
    """a class for the ball"""
    def __init__(self, color = 'white'):
        self.center = [WIDTH/2, HEIGHT/2]
        self.radius = BALL_RADIUS
        self.vel = [0, 0]
        self.color = color
        self.go_left = random.choice([True, False])

    def restart(self):
        self.center = [WIDTH/2, HEIGHT/2]
        self.vel[0] = (2.0 + random.random() * 2.0)	* BALL_VEL_SCALE	# range from 2 - 4
        self.vel[0] *= (-1) ** self.go_left
        self.vel[1] = (-(1.0 + random.random())) * BALL_VEL_SCALE		# range from 1 - 2

    def update(self, l_pad, r_pad):
        btwn_top_bot = BALL_RADIUS < (self.center[1] + self.vel[1]) < HEIGHT - BALL_RADIUS
        if not btwn_top_bot:
            self.vel[1] *= -1

        touch_l_gutter = (self.center[0] + self.vel[0]) < L_GUTTER + BALL_RADIUS
        touch_r_gutter = (self.center[0] + self.vel[0]) > R_GUTTER - BALL_RADIUS
        on_l_pad = l_pad.get_bot() < self.center[1] < l_pad.get_top()
        on_r_pad = r_pad.get_bot() < self.center[1] < r_pad.get_top()

        if not(touch_l_gutter or touch_r_gutter):
            self.center[0] += self.vel[0]
            self.center[1] += self.vel[1]
        elif touch_l_gutter and not on_l_pad:
            r_pad.scored()
            self.go_left = False
            self.restart()
        elif touch_r_gutter and not on_r_pad:
            l_pad.scored()
            self.go_left = True
            self.restart()
        else:
            self.vel[0] *= -1.1

    def draw(self, canvas):
        canvas.draw_circle(self.center, self.radius, 1, self.color, self.color)

class Paddle:
    """a class to control paddles"""
    def __init__(self, name, x_pos, x_score, color = 'white'):
        self.name = name
        self.center = [x_pos, HEIGHT/2]
        self.score_pos = (x_score, PAD_HEIGHT/2)
        self.up = False
        self.down = False
        self.vel = 0.0
        self.color = color
        self.score = 0

    def __str__(self):
        return self.name

    def get_top(self):
        return self.center[1] + PAD_HEIGHT/2

    def get_bot(self):
        return self.center[1] - PAD_HEIGHT/2

    def scored(self):
        self.score += 1

    def reset_score(self):
        self.score = 0

    def get_corners(self):
        lft = self.center[0] - PAD_WIDTH/2
        rgt = self.center[0] + PAD_WIDTH/2
        top = self.center[1] + PAD_HEIGHT/2
        bot = self.center[1] - PAD_HEIGHT/2
        return [[lft, top], [rgt, top], [rgt, bot], [lft, bot]]

    def move_up(self):
        self.up = not self.up

    def move_down(self):
        self.down = not self.down

    def update(self):
        self.vel = (int(self.down) - int(self.up)) * PADDLE_SPD
        btwn_stops = PAD_STOP < (self.center[1] + self.vel) < HEIGHT - PAD_STOP
        if btwn_stops:
            self.center[1] += self.vel

    def draw(self, canvas):
        canvas.draw_polygon(self.get_corners(), 1, self.color, self.color)
        canvas.draw_text(str(self.score), self.score_pos, 20, self.color)

class Arena:
    """a class to define the playing area"""
    def __init__(self, color = 'white'):
        self.size = (WIDTH, HEIGHT)
        self.color = color

    def draw(self, canvas):
        center_x = WIDTH/2

        canvas.draw_line([center_x, 0],[center_x, HEIGHT], 1, self.color)
        canvas.draw_line([L_GUTTER, 0],[L_GUTTER, HEIGHT], 1, self.color)
        canvas.draw_line([R_GUTTER, 0],[R_GUTTER, HEIGHT], 1, self.color)

# Instantiate objects
ball = Ball()
l_pad = Paddle('left', 0 + PAD_WIDTH/2, WIDTH/4)
r_pad = Paddle('right', WIDTH - PAD_WIDTH/2, 3*WIDTH/4)
arena = Arena()

# Define event handlers
def new_game(ball):
    ball.restart()
    l_pad.reset_score()
    r_pad.reset_score()

def draw(canvas):
    ball.update(l_pad, r_pad)
    l_pad.update()
    r_pad.update()

    arena.draw(canvas)
    ball.draw(canvas)
    l_pad.draw(canvas)
    r_pad.draw(canvas)

KEY_MAP = {}
for key in simplegui.KEY_MAP:
    KEY_MAP[simplegui.KEY_MAP[key]] = key
KEY_BINDINGS = {
    'W': l_pad.move_up,
    'S': l_pad.move_down,
    'up': r_pad.move_up,
    'down': r_pad.move_down,
    }

def keydown(key):
    try:
        KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

def keyup(key):
    try:
        KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

def reset_button():
    new_game(ball)

# Create frame, Register events
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', reset_button)

# Start frame
new_game(ball)
frame.start()
