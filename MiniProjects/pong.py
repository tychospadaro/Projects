# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PADDLE_VEL = 3.5

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0.0, 0.0]
    ball_vel[0] = 2.0 + random.random() * 2.0	# range from 2 - 4
    ball_vel[1] = -(1.0 + random.random())		# range from 1 - 2
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]

def pad_pts(center):
    """given paddle center (as [x,y];
       return a list of points representing paddle corners"""
    u_l = [center[0] + HALF_PAD_WIDTH, center[1] + HALF_PAD_HEIGHT]
    b_l = [center[0] - HALF_PAD_WIDTH, center[1] + HALF_PAD_HEIGHT]
    b_r = [center[0] - HALF_PAD_WIDTH, center[1] - HALF_PAD_HEIGHT]
    u_r = [center[0] + HALF_PAD_WIDTH, center[1] - HALF_PAD_HEIGHT]
    return [u_l, b_l, b_r, u_r]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    direction = random.choice([LEFT, RIGHT])
    score1, score2 = 0, 0
    paddle1_pos = [float(HALF_PAD_WIDTH), float(HEIGHT / 2)]
    paddle2_pos = [float(WIDTH - HALF_PAD_WIDTH), float(HEIGHT / 2)]
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if ball_pos[1] <= BALL_RADIUS or \
        ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]		# ceiling/floor collision check
    ball_pos[0] += ball_vel[0]			# move ball (x)
    ball_pos[1] += ball_vel[1]			# move ball (y)
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel > HALF_PAD_HEIGHT and \
       paddle1_pos[1] + paddle1_vel < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel	# check ceil/floor, move paddle1
    if paddle2_pos[1] + paddle2_vel > HALF_PAD_HEIGHT and \
       paddle2_pos[1] + paddle2_vel < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel	# check ceil/floor, move paddle2
    # draw paddles
    paddle1 = canvas.draw_polygon(pad_pts(paddle1_pos), 1, 'white', 'white')
    paddle2 = canvas.draw_polygon(pad_pts(paddle2_pos), 1, 'white', 'white')

    # determine whether paddle and ball collide
    strike_left = ball_pos[0] <= PAD_WIDTH + BALL_RADIUS
    pad1_ball_overlap = ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT \
                    and ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT
    strike_right = ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS)
    pad2_ball_overlap = ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT \
                    and ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT

    if strike_left and pad1_ball_overlap:	# strike left bumper
        ball_vel[0] = -1.1 * ball_vel[0]	# reverse & speed up ball
        ball_vel[1] = 1.1 * ball_vel[1]		#
    elif strike_left:						# strike left gutter
        score2 += 1							# score for Right
        spawn_ball(RIGHT)					# respawn right
    elif strike_right and pad2_ball_overlap:# strike right bumper
        ball_vel[0] = -1.1 * ball_vel[0]	# reverse & speed up ball
        ball_vel[1] = 1.1 * ball_vel[1]		#
    elif strike_right:						# strike right gutter
        score1 += 1							# score for Left
        spawn_ball(LEFT)					# respawn left

    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4, 40), 20, 'white')
    canvas.draw_text(str(score2), (3*WIDTH/4, 40), 20, 'white')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= PADDLE_VEL	# paddle1 up
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += PADDLE_VEL	# paddle1 down
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= PADDLE_VEL	# paddle2 up
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += PADDLE_VEL	# paddle2 down

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += PADDLE_VEL	# paddle1 stop/down
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= PADDLE_VEL	# paddle1 stop/up
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel += PADDLE_VEL	# paddle2 stop/down
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= PADDLE_VEL	# paddle2 stop/up

def click():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', click)

# start frame
new_game()
frame.start()
