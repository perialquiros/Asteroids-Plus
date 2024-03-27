#Implements the ships and bullet targetting player
from math import *
import pygame
import random
from sprites import *
from config import *
import sys


class Ships(pygame.sprite.Sprite):
    # create the ship
    def __init__(self):
        pygame.sprite.pygame.sprite.Sprite.__init__(self)

        # adjust imported image
        og_image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(og_image, (30,20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y, self.direction = self.rand_entry()

        # sets the ship speed of movement
        self.speed = 0.5

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
        
    def move(self):
        if self.direction == 'top':
            self.rect.y -= 1
        elif self.direction == 'bottom':
            self.rect.y += 1
        elif self.direction == 'left':
            self.rect.x -= 1
        elif self.direction == 'right':
            self.rect.x += 1
        elif self.direction == 'top_left':
            self.rect.x -= 1
            self.rect.y -= 1
        elif self.direction == 'top_right':
            self.rect.x += 1
            self.rect.y -= 1
        elif self.direction == 'bottom_left':
            self.rect.x -= 1
            self.rect.y += 1
        elif self.direction == 'bottom_right':
            self.rect.x += 1
            self.rect.y += 1
           