# Basic infrastructure for Bubble Shooter

import simplegui
import random
import math

# Global constants
WIDTH = 800
HEIGHT = 600
FIRING_POSITION = [WIDTH // 2, HEIGHT]
FIRING_LINE_LENGTH = 60
FIRING_ANGLE_VEL_INC = 0.02
BUBBLE_RADIUS = 20
COLOR_LIST = ["Red", "Green", "Blue", "White"]
BUBBLE_SPD = 0.2
FIRING_SOUND = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/Collision8-Bit.ogg")

# global variables
firing_angle = math.pi / 2
firing_angle_vel = 0

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# class defintion for Bubbles
class Bubble:
    def __init__(self):
        self.pos = FIRING_POSITION
        self.vel = [0,0]
        self.color = random.choice(COLOR_LIST)
        self.radius = BUBBLE_RADIUS
        self.sound = FIRING_SOUND
        self.fired = False

    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1,
                           self.color, self.color)
    def update(self):
        if self.vel == [0, 0]:				# stopped
            return
        elif self.pos[1] + self.vel[0] <= BUBBLE_RADIUS:	# hit top
            self.vel = [0,0]
            self.pos[1] = self.radius
            return
        else:								# move, then check side
            self.pos = [self.pos[0] + self.vel[0],
                        self.pos[1] + self.vel[1]]
        if not(self.radius < self.pos[0] < WIDTH - self.radius):
            self.vel[0] *= -1

    def fire_bubble(self, vel):
        self.vel = vel
        self.fired = True
        self.sound.play()

    def collide(self, bubble):
        distance = dist(self.pos, bubble.pos)
        if distance <= 2 * self.radius:
            self.vel = [0,0]
            return True
        else:
            return False


    def is_fired(self):
        return self.fired

# a class definition for the shooter
class Shooter:
    def __init__(self):
        self.length = FIRING_LINE_LENGTH
        self.angle = firing_angle
        self.angle_vel = firing_angle_vel
        self.anchor = FIRING_POSITION
        self.left = False
        self.right = False
        self.active_bubble = Bubble()
        self.stuck_bubbles = set()

    def draw(self, canvas):
        canvas.draw_line(self.tip, self.anchor, 2, 'lime')
        self.active_bubble.draw(canvas)
        map(lambda bubble: bubble.draw(canvas), self.stuck_bubbles)

    def update(self):
        self.angle_vel = (int(self.left) - int(self.right))\
                         * FIRING_ANGLE_VEL_INC
        new_angle = self.angle + self.angle_vel
        if 0 < new_angle < math.pi:
            self.angle = new_angle
            self.get_tip()
        if self.active_bubble.is_fired():
            self.active_bubble.update()
            map(lambda stuck: self.active_bubble.collide(stuck), self.stuck_bubbles)
            self.reload_bubble()

    def get_tip(self):
        angle_vector = angle_to_vector(self.angle)
        self.tip = [self.anchor[0] + angle_vector[0] * self.length,
                    self.anchor[1] - angle_vector[1] * self.length]

    def move_left(self):
        self.left = not self.left

    def move_right(self):
        self.right = not self.right

    def launch(self):
        if self.active_bubble.fired == False:
            fire_vel = [(self.tip[0] - self.anchor[0]) * BUBBLE_SPD,
                        (self.tip[1] - self.anchor[1]) * BUBBLE_SPD]
            self.active_bubble.fire_bubble(fire_vel)

    def reload_bubble(self):
        if self.active_bubble.vel == [0, 0]:
            self.stuck_bubbles.add(self.active_bubble)
            self.active_bubble = Bubble()

the_shooter = Shooter()

# define keyhandlers to control firing_angle
KEY_MAP = {}
for key in simplegui.KEY_MAP:
    KEY_MAP[simplegui.KEY_MAP[key]] = key
KEY_BINDINGS = {
    'A': the_shooter.move_left,
    'D': the_shooter.move_right,
    'left': the_shooter.move_left,
    'right': the_shooter.move_right,
    'space': the_shooter.launch,
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

# define draw handler
def draw(canvas):
    global firing_angle, a_bubble, bubble_stuck

    # update firing angle
    the_shooter.update()

    # draw firing line
    the_shooter.draw(canvas)


    # update a_bubble and check for sticking



    # draw a bubble and stuck bubbles

# create frame and register handlers
frame = simplegui.create_frame("Bubble Shooter", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# create initial bubble and start frame


frame.start()
