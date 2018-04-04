# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SHIP_ANGLE_VEL = 0.1
SHIP_ACCEL = 0.8
FRICTION = 0.025
ROCK_VEL_LIMIT = 2
ROCK_ROT_LIMIT = 0.1
MISSILE_SPD = 3

score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.thrust_sound = sound
        self.rotate_l = False
        self.rotate_r = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    def fire_thrust(self):
        self.thrust = not self.thrust
        self.image_center[0] = (self.image_center[0] + 90)%180
        if self.thrust:
            self.thrust_sound.play()
        else:
            self.thrust_sound.rewind()

    def rotate_left(self):
        self.rotate_l = not self.rotate_l
    def rotate_right(self):
        self.rotate_r = not self.rotate_r

    def update(self):
        self.angle_vel = (int(self.rotate_r) - int(self.rotate_l))\
                         * SHIP_ANGLE_VEL
        self.angle += self.angle_vel

        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * SHIP_ACCEL
            self.vel[1] += forward[1] * SHIP_ACCEL

        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT

    def get_tip(self):
        pos_x, pos_y = self.pos
        unit_x, unit_y = angle_to_vector(self.angle)
        length = self.radius
        return [pos_x + unit_x * length,
                pos_y + unit_y * length]

    def get_missile_vel(self):
        vel_x, vel_y = self.vel
        unit_x, unit_y = angle_to_vector(self.angle)
        tot_x = vel_x + (unit_x * MISSILE_SPD)
        tot_y = vel_y + (unit_y * MISSILE_SPD)
        return [tot_x, tot_y]

    def fire_missile(self):
        global a_missile
        nose = self.get_tip()
        velocity = self.get_missile_vel()
        a_missile = Sprite(nose, velocity, 0, 0, missile_image, missile_info, missile_sound)



# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT



def centered_random(center, dist):
    return random.random() * 2 * dist + center - dist

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    x_pos = random.random() * WIDTH
    y_pos = random.random() * HEIGHT
    x_vel = centered_random(0, ROCK_VEL_LIMIT)
    y_vel = centered_random(0, ROCK_VEL_LIMIT)
    ang = centered_random(0, math.pi)
    ang_vel = centered_random(0, ROCK_ROT_LIMIT)

    a_rock = Sprite([x_pos, y_pos], [x_vel, x_vel], ang,
                    ang_vel, asteroid_image, asteroid_info)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, -0.02, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    # draw score and lives
    canvas.draw_text('Lives', [45,50], 20, 'white', 'sans-serif')
    canvas.draw_text(str(lives), [45,70], 20, 'white', 'sans-serif')
    canvas.draw_text('Score', [700,50], 20, 'white', 'sans-serif')
    canvas.draw_text(str(score), [700,70], 20, 'white', 'sans-serif')

KEY_MAP = {}
for key in simplegui.KEY_MAP:
    KEY_MAP[simplegui.KEY_MAP[key]] = key
KEY_BINDINGS = {
    'W': my_ship.fire_thrust,
    'A': my_ship.rotate_left,
    'D': my_ship.rotate_right,
    'up': my_ship.fire_thrust,
    'left': my_ship.rotate_left,
    'right': my_ship.rotate_right,
    'space': my_ship.fire_missile,
    }

def keydown(key):
    try:
        KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

def keyup(key):
    try:
        if KEY_MAP[key] is not 'space':
            KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
