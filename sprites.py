import pygame
from config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups) #add player to all sprites group

        #Player position based on tile
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #PLayer size - one tile
        self.width = TILESIZE
        self.height = TILESIZE

        #temporary value at init
        self.x_change = 0
        self.y_change = 0

        #create player (TEMPORARY look)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        # self.image.get_rect() returns a new rectangle covering the entire surface of `self.image`. This rectangle (rect) is used to position the sprite on the screen.
        # It's important for collision detection and rendering the sprite at its current position.
        self.rect = self.image.get_rect()

        #set player's rect x, y positions
        self.rect.x = self.x
        self.rect.y = self.y

def update(self):
    pass

def movement(self):
    pass