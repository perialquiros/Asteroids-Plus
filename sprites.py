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

        #create player (TEMPORARY look)
        self.image = pygame.image.load('ships/ship-a1.png').convert_alpha()

        # self.image.get_rect() returns a new rectangle covering the entire surface of `self.image`. This rectangle (rect) is used to position the sprite on the screen.
        # It's important for collision detection and rendering the sprite at its current position.
        self.rect = self.image.get_rect()

        #set player's rect x, y positions
        self.rect.x = self.x
        self.rect.y = self.y

        #temporary value at init
        self.x_change = 0
        self.y_change = 0
        self.angle = 0
        
        
     #update player sprite
    def update(self):

        #update movement
        self.rotate()
        self.movement()
        #update player rect position based on return value of movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        #reset _change vars
        self.x_change = 0
        self.y_change = 0

    def turnLeft(self):
        self.angle += 5 # Adjust rotation speed as needed
        if self.angle > 360:
            self.angle -= 360

    def turnRight(self):
        self.angle -= 5  # Adjust rotation speed as needed
        if self.angle < 0:
            self.angle += 360

    def moveForward(self):
        rad_angle = math.radians(self.angle)  # Convert angle to radians
        self.x_change += PLAYER_SPEED * math.cos(rad_angle)
        self.y_change += PLAYER_SPEED * math.sin(rad_angle)

    def rotate(self):
        original_center = self.rect.center  # Save the sprite's center
        self.image = pygame.transform.rotate(pygame.image.load('ships/ship-a1.png').convert_alpha(), -self.angle)  # Rotate the original image
        self.rect = self.image.get_rect(center=original_center)  # Create a new rect with the old center

    #function to make player move based on arrow keys
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turnLeft()
        if keys[pygame.K_RIGHT]:
            self.turnRight()
        if keys[pygame.K_UP]:
            self.moveForward()