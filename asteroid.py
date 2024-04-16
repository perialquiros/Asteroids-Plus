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
            _, _, self.move_direction = self.rand_entry()
        # if we are spawning asteroids out of bounds (for asteroid_alg())
        else:
            self.rect.x, self.rect.y, self.move_direction = self.rand_entry() 

        # Set up the speed and angle
        self.speed = ASTEROID_SPEED
        self.set_angle_and_velocity()

    # constantly update asteroid movement and wrap around
    def update(self):
        self.move()
        self.wrap_around_screen()

    # generate the random entry position
    def rand_entry(self):
        side = random.choice(['top', 'bottom', 'left', 'right','top_left', 'top_right', 'bottom_left', 'bottom_right'])
        if side == 'top':
            return random.randint(0, WIN_WIDTH - self.rect.width), -self.rect.height, 'bottom'
        elif side == 'bottom':
            return random.randint(0, WIN_WIDTH - self.rect.width), WIN_HEIGHT, 'top'
        elif side == 'left':
            return -self.rect.width, random.randint(0, WIN_HEIGHT - self.rect.height), 'right'
        elif side == 'right':
            return WIN_WIDTH, random.randint(0, WIN_HEIGHT - self.rect.height), 'left'
        elif side == 'top_left':
            return -self.rect.width, -self.rect.height, 'bottom_right'
        elif side == 'top_right':
            return WIN_WIDTH, -self.rect.height, 'bottom_left'
        elif side == 'bottom_left':
            return -self.rect.width, WIN_HEIGHT, 'top_right'
        elif side == 'bottom_right':
            return WIN_WIDTH, WIN_HEIGHT, 'top_left'

    # randomly set an angle for the asteroid to move
    def set_angle_and_velocity(self):
        # Set angle based on move_direction
        if self.move_direction in ['top', 'bottom']:
            self.angle = random.uniform(-45, 45)  # For top and bottom, limit the angle to 45 degrees left or right
        elif self.move_direction in ['left', 'right']:
            self.angle = random.uniform(135, 225)  # For left and right, aim mostly up or down
        else:  # For corner spawns, use larger angle ranges
            angle_ranges = {
                'top_left': (45, 135),
                'top_right': (-45, 45),
                'bottom_left': (225, 315),
                'bottom_right': (135, 225)
            }
            self.angle = random.uniform(*angle_ranges[self.move_direction])
        
        # Update velocity based on the angle
        rad_angle = math.radians(self.angle)
        if self.move_direction in ['top', 'bottom_right', 'top_right']:
            self.x_change = self.speed * math.cos(rad_angle)
            self.y_change = self.speed * math.sin(rad_angle)
        else:  # Reverse direction for bottom and left spawns
            self.x_change = -self.speed * math.cos(rad_angle)
            self.y_change = -self.speed * math.sin(rad_angle)

    # move asteroid based on speed
    def move(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

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
    def check_collision(self, group, ship_bullets):
        for bullet in group: 
            if pygame.sprite.collide_circle(self, bullet):
                self.kill()
                bullet.kill()
        for bullet in ship_bullets: 
            if pygame.sprite.collide_circle(self, bullet):
                self.kill()
                bullet.kill()
                