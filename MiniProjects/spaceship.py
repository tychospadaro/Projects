# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
SHIP_ANGLE_VEL = 0.1
SHIP_ACCEL = 0.5
FRICTION = 0.025
ROCK_VEL_LIMIT = 2
ROCK_ROT_LIMIT = 0.1
MISSILE_SPD = 5

started = False
score = 0
hi_score = 0
lives = 3
time = 0
rocks = set()
explosions = set()

muted = False

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
sounds = [soundtrack, missile_sound, ship_thrust_sound, explosion_sound]

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
# soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def centered_random(center, dist):
    return random.random() * 2 * dist + center - dist

def vector_vector_update(vector, values, operator):
    for idx, val in enumerate(vector):
        if operator == '+':
            vector[idx] += values[idx]
        elif operator == '-':
            vector[idx] -= values[idx]
        elif operator == '*':
            vector[idx] *= values[idx]
        elif operator == '%':
            vector[idx] %= values[idx]
        else:
            print operator + ' not yet supported'

def vector_scalar_update(vector, value, operator):
    for idx, val in enumerate(vector):
        if operator == '+':
            vector[idx] += value
        elif operator == '-':
            vector[idx] -= value
        elif operator == '*':
            vector[idx] *= value
        elif operator == '%':
            vector[idx] %= value
        else:
            print operator + ' not yet supported'

def group_collide(fragile_object, rocks):
    removal_set = set()
    for rock in list(rocks):
        if rock.collide(fragile_object):
            removal_set.add(rock)
    rocks.difference_update(removal_set)
    if len(removal_set) > 0:
        explosion_spawner(fragile_object.get_position())
    return len(removal_set)

def group_group_collide(missiles, rocks):
    score = 0
    for missile in list(missiles):
        hit = group_collide(missile, rocks)
        if hit > 0:
            missiles.remove(missile)
            score += hit
    return score

def despawner(sprites):
    despawn_expired = filter(lambda sprite: sprite.despawn(), sprites)
    sprites.difference_update(despawn_expired)

def group_update_draw_despawn(group, canvas):
    map(lambda item: item.update(), group)
    map(lambda item: item.draw(canvas), group)
    despawner(group)

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
        self.missiles = set()

    def draw(self,canvas):
        group_update_draw_despawn(self.missiles, canvas)
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        int_rotation = (int(self.rotate_r) - int(self.rotate_l))
        self.angle_vel = int_rotation * SHIP_ANGLE_VEL
        self.angle += self.angle_vel

        if self.thrust:
            forward = angle_to_vector(self.angle)
            vector_scalar_update(forward, SHIP_ACCEL, '*')
            vector_vector_update(self.vel, forward, '+')
        vector_scalar_update(self.vel, (1-FRICTION), '*')

        vector_vector_update(self.pos, self.vel, '+')
        vector_vector_update(self.pos, [WIDTH, HEIGHT], '%')

    def rotate_left(self):
        self.rotate_l = not self.rotate_l

    def rotate_right(self):
        self.rotate_r = not self.rotate_r

    def fire_thrust(self):
        self.thrust = not self.thrust
        self.image_center[0] = (self.image_center[0] + 90)%180
        if self.thrust:
            self.thrust_sound.play()
        else:
            self.thrust_sound.rewind()

    def fire_missile(self):
        nose = self.get_tip()
        velocity = self.get_missile_vel()
        self.missiles.add(Sprite(nose, velocity, 0, 0, missile_image, missile_info, missile_sound))

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    # internal functions
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

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = list(info.get_center())
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def __repr__(self):
        if self.radius == 3:
            return 'missile'
        elif self.radius == 40:
            return 'asteroid'
        else:
            position = str(list(self.pos))
            age = str(self.age)
            return position + ' ' + age

    def draw(self, canvas):
        if self.animated:
            print self.__repr__
            self.image_center[0] = self.image_center[0] + self.image_size[0]
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        vector_vector_update(self.pos, self.vel, '+')
        vector_vector_update(self.pos, [WIDTH, HEIGHT], '%')
        self.age += 1

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        crash_dist = self.radius + other_object.get_radius()
        distance = dist(self.pos, other_object.get_position())

        if distance < crash_dist:
            return True
        else:
            return False

    def despawn(self):
        return self.age > self.lifespan

# timer handler that spawns a rock
def rock_spawner():
    if len(rocks) > 12:
        return

    score_mod = 0.5 * score
    x_pos = random.random() * WIDTH
    y_pos = random.random() * HEIGHT
    x_vel = centered_random(0, ROCK_VEL_LIMIT + score_mod)
    y_vel = centered_random(0, ROCK_VEL_LIMIT + score_mod)
    ang = centered_random(0, math.pi)
    ang_vel = centered_random(0, ROCK_ROT_LIMIT)
    new_rock = Sprite([x_pos, y_pos], [x_vel, x_vel], ang,
                    ang_vel, asteroid_image, asteroid_info)
    if new_rock.collide(my_ship):
        rock_spawner()
    else:
        rocks.add(new_rock)

def explosion_spawner(center):
    new_explosion = Sprite(center, [0, 0], 0, 0, explosion_image,
                           explosion_info, explosion_sound)
    explosions.add(new_explosion)

# initialize ship and rock
def restart():
    global started, score, lives, my_ship, rocks
    started = False
    soundtrack.rewind()
    score = 0
    lives = 3
    my_ship.pos = [WIDTH / 2, HEIGHT / 2]
    my_ship.vel = [0, 0]
    my_ship.angle = 0
    rocks = set()
    rock_spawner()

def mute():
    global muted
    if muted == False:
        muted = True
        map(lambda sound: sound.set_volume(0), sounds)
    else:
        muted = False
        map(lambda sound: sound.set_volume(1), sounds)
        missile_sound.set_volume(0.5)

def draw(canvas):
    global time, started, lives, score, hi_score

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], splash_info.get_size())
        canvas.draw_text('High Score: '+str(hi_score), [250,400], 20, 'white', 'sans-serif')
        return

    # update ship and sprites
    my_ship.update()
    my_ship.draw(canvas)
    group_update_draw_despawn(rocks, canvas)
    group_update_draw_despawn(explosions, canvas)

    score += group_group_collide(my_ship.missiles, rocks)

    if group_collide(my_ship, rocks) > 0:
        lives -= 1

    if lives <=0:
        hi_score = max(score, hi_score)
        restart()

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
    'M': mute,
    'up': my_ship.fire_thrust,
    'left': my_ship.rotate_left,
    'right': my_ship.rotate_right,
    'space': my_ship.fire_missile,
    }

KEY_TOGGLES = ['space', 'M']

def keydown(key):
    try:
        KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

def keyup(key):
    try:
        if KEY_MAP[key] not in KEY_TOGGLES:
            KEY_BINDINGS[KEY_MAP[key]]()
    except KeyError:
        pass

def click(pos):
    global started
    if not started:
        started = True
        soundtrack.play()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
