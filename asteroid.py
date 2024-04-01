import pygame
from config import *
from sprites import *
import math
import random

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, game, x, y, size):

        self.game = game
        self._layer = ASTEROID_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        if size == BIG_ASTEROID_SIZE:
            image = random.choice(['Images/asteroid-big/big-a.png', 'Images/asteroid-big/big-b.png', 'Images/asteroid-big/big-c.png'])
        elif size == MED_ASTEROID_SIZE:
            image = random.choice(['Images/asteroid-med/med-a.png', 'Images/asteroid-med/med-b.png', 'Images/asteroid-med/med-c.png'])
        else:
            image = random.choice(['Images/asteroid-small/small-a.png', 'Images/asteroid-small/small-b.png', 'Images/asteroid-small/small-c.png'])

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()

        self.width = size
        self.height = size

         # Initialize movement direction based on spawn side
        self.rect.x, self.rect.y, self.move_direction = self.rand_entry()

        # Set up the speed and angle
        self.speed = ASTEROID_SPEED
        self.set_angle_and_velocity()


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

    def move(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def wrap_around_screen(self):
        if self.rect.right < 0:
            self.rect.left = WIN_WIDTH
        if self.rect.left > WIN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = WIN_HEIGHT
        if self.rect.top > WIN_HEIGHT:
            self.rect.bottom = 0