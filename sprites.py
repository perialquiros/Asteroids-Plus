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

        # player position based on tile
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # player size - one tile
        self.width = TILESIZE
        self.height = TILESIZE

        # temporary value at init
        self.x_change = 0
        self.y_change = 0

        # create player (TEMPORARY look)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        # self.image.get_rect() returns a new rectangle covering the entire surface of `self.image`. This rectangle (rect) is used to position the sprite on the screen.
        # it's important for collision detection and rendering the sprite at its current position.
        self.rect = self.image.get_rect()

        # set player's rect x, y positions
        self.rect.x = self.x
        self.rect.y = self.y
        
     #update player sprite
    def update(self):

        #update movement
        self.movement()
        #update player rect position based on return value of movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        #reset _change vars
        self.x_change = 0
        self.y_change = 0

    #function to make player move based on arrow keys
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'