import pygame
from config import *
from player import *
import math
import random

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, game, size, x=None, y=None):
        pygame.init()
        self.game = game
        self._layer = ASTEROID_LAYER
        # add asteroid to sprite groups
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.size = size
        # randomly choose asteroid image based on its size
        if size == BIG_ASTEROID_SIZE:
            image = random.choice(['Images/asteroid-big/big-a.png', 'Images/asteroid-big/big-b.png', 'Images/asteroid-big/big-c.png'])
        elif size == MED_ASTEROID_SIZE:
            image = random.choice(['Images/asteroid-med/med-a.png', 'Images/asteroid-med/med-b.png', 'Images/asteroid-med/med-c.png'])
        else:
            image = random.choice(['Images/asteroid-small/small-a.png', 'Images/asteroid-small/small-b.png', 'Images/asteroid-small/small-c.png'])
        # load and scale asteroid based on size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size, size))
        # init asteroid rect
        self.rect = self.image.get_rect()
        # init asteroid width and height
        self.width = size
        self.height = size

        # init rect x and y based on input
        # if we are spawning asteroids at a specfic spot (when asteroid is splitting)
        if x is not None and y is not None:
            self.rect.x = x
            self.rect.y = y
            self.side = None
        # if we are spawning asteroids out of bounds (for asteroid_alg())
        else:
            self.spawn_random_loc()

        self.floating_x = float(self.rect.x)
        self.floating_y = float(self.rect.y)
        # Set up the speed and angle
        self.speed = ASTEROID_SPEED
        self.set_random_dir()
        

    # constantly update asteroid movement and wrap around
    def update(self):
        self.move()
        self.wrap_around_screen()

    # generate the random entry position
    def spawn_random_loc(self):
        self.side = random.choice(['top', 'bottom', 'left', 'right'])
        if self.side == 'top':
            self.rect.x = random.randrange(WIN_WIDTH)
            self.rect.y = -self.size
        elif self.side == 'bottom':
            self.rect.x = random.randrange(WIN_WIDTH)
            self.rect.y = WIN_HEIGHT
        elif self.side == 'left':
            self.rect.x = -self.size
            self.rect.y = random.randrange(WIN_HEIGHT)
        elif self.side == 'right':
            self.rect.x = WIN_WIDTH
            self.rect.y = random.randrange(WIN_HEIGHT)

    def set_random_dir(self):

        angle_ranges = {
            'top': (225,315), #Downward angles
            'bottom': (45, 135), #Upward angles
            'left': (-45,45), # Rightward angles
            'right': (135, 225) #Leftward angles
        }
        if self.side in angle_ranges:
            angle = random.uniform(*angle_ranges[self.side])
        else:
            angle = random.uniform(0, 360)

        if self.side == 'left':
            angle = (angle + 360) % 360

        speed = ASTEROID_SPEED
        rad_angle = math.radians(angle)
        self.x_change = speed * math.cos(rad_angle)
        self.y_change = speed * math.sin(rad_angle)


    # move asteroid based on speed
    def move(self):
        self.floating_x += self.x_change
        self.floating_y += self.y_change
        self.rect.x = int(self.floating_x)
        self.rect.y = int(self.floating_y)
        #self.rect.x += self.x_change
        #self.rect.y += self.y_change

    # ensure asteroid comes back around when moving out of screen
    def wrap_around_screen(self):
        if self.rect.right < 0:
            self.rect.left = WIN_WIDTH
        if self.rect.left > WIN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = WIN_HEIGHT
        if self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0

    # get the size below of the current asteroid - use for splitting - 0 means no splitting
    def getSizeBelow(self):
        if self.width == BIG_ASTEROID_SIZE:
            return MED_ASTEROID_SIZE
        elif self.width == MED_ASTEROID_SIZE:
            return SM_ASTEROID_SIZE
        else:
            return 0
        
    # method to check collision between the asteroid and another sprite - used in menu.py
    def check_collision(self, group):
        for bullet in group: 
            if pygame.sprite.collide_circle(self, bullet):
                self.kill()
                bullet.kill()
                ASTEROID_CHANNEL.play(ASTEROID_MUSIC)
                return True
        return False