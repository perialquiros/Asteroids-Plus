#Implements the ships and bullet targetting player
from math import *
import pygame
import random
from sprites import *
from config import *
import sys


class Ships(pygame.sprite.Sprite):

    # create the ship
    def __init__(self, all_sprites, bullets):
        super().__init__()
        self.all_sprites = all_sprites
        self.bullets = bullets
        
        # adjust imported image
        og_image = pygame.image.load('Images/ship.png')
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
            if self.rect.bottom < 0: # check if the ship exits the top edge
                self.rect.y = WIN_HEIGHT
                self.rect.x = WIN_WIDTH - self.rect.x
        elif self.direction == 'bottom':
            self.rect.y += 1
            if self.rect.top > WIN_HEIGHT:
                self.rect.y = 0
                self.rect.x = WIN_WIDTH - self.rect.x
        elif self.direction == 'left':
            self.rect.x -= 1
            if self.rect.right < 0:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = WIN_WIDTH
        elif self.direction == 'right':
            self.rect.x += 1
            if self.rect.left > WIN_WIDTH:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = 0
        elif self.direction == 'top_left':
            self.rect.x -= 1
            self.rect.y -= 1
            if self.rect.bottom < 0: 
                self.rect.y = WIN_HEIGHT
                self.rect.x = WIN_WIDTH - self.rect.x
            if self.rect.right < 0:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = WIN_WIDTH
        elif self.direction == 'top_right':
            self.rect.x += 1
            self.rect.y -= 1
            if self.rect.bottom < 0: 
                self.rect.y = WIN_HEIGHT
                self.rect.x = WIN_WIDTH - self.rect.x
            if self.rect.left > WIN_WIDTH:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = 0
        elif self.direction == 'bottom_left':
            self.rect.x -= 1
            self.rect.y += 1
            if self.rect.top > WIN_HEIGHT:
                self.rect.y = 0
                self.rect.x = WIN_WIDTH - self.rect.x
            if self.rect.right < 0:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = WIN_WIDTH
        elif self.direction == 'bottom_right':
            self.rect.x += 1
            self.rect.y += 1
            if self.rect.top > WIN_HEIGHT:
                self.rect.y = 0
                self.rect.x = WIN_WIDTH - self.rect.x
            if self.rect.left > WIN_WIDTH:
                self.rect.y = WIN_HEIGHT - self.rect.y
                self.rect.x = 0
    
    def shoot_bullet(self, player_rect):
        # Calculate the direction vector towards the player
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(abs(dx), abs(dy), 1)  # Avoid division by zero
        direction = dx / distance, dy / distance

        # Spawn the bullet at the ship's current position
        bullet = Bullet(self.rect.centerx, self.rect.centery, direction)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    
    # initialize bullet as a new sprite
    def __init__(self, x, y, direction):
        super().__init__()

        # adjust imported image
        bullet_image = pygame.image.load('Images/bullet.png')
        self.image = pygame.transform.scale(bullet_image, (15,8))
        self.rect = self.image.get_rect(center=(x, y)) #spawns bullet at the location of the ship
        self.direction = direction
        self.speed = PLAYER_SPEED/2
    
    def update(self):
        # continue to move in the direction of the player
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

           