import math
import pygame
import random
import config
import sys

class Powerups(pygame.sprite.Sprite):

    # create the powerups
    def __init__(self, all_sprites, player, screen):
        super().__init__()
        self.all_sprites = all_sprites
        self.player = player
        self.screen = screen
        self.collision = False

        #load all powerup images and random chooses one
        image_paths = ['Images/powerups/shield.png', 'Images/powerups/plus.jpeg', 'Images/powerups/bomb.png']
        self.images = [pygame.image.load(path) for path in image_paths]
        self.image = random.choice(self.images)  # Randomly choose one image
        self.rect = self.image.get_rect()
        self.rand_placement()

    def rand_placement(self):
        self.rect.x = random.randint(0, config.WIN_WIDTH)
        self.rect.y = random.randint(0, config.WIN_HEIGHT)

    def shield_funct(self):
        self.player.damage_loop += 5000 #allows 5 seconds of invulnerability
    
    def plus_funct(self):
        config.PLAYER_LIVES += 1
    
    def bomb_funct(self):
        self.screen.fill((0, 0, 0))  # Fill with black color

        # Redraw only the player sprite
        self.all_sprites.draw(self.screen)

        # Update the display
        pygame.display.flip()

    def update(self):
        distance = math.sqrt((self.rect.centerx - self.player.rect.centerx) ** 2 + (self.rect.centery - self.player.rect.centery) ** 2)
        collision_threshold = max(self.rect.width, self.rect.height) / 2 + max(self.player.rect.width, self.player.rect.height) / 2 - 2 * config.TILESIZE
            
        # Check if within collision threshold to obtain the powerup
        if distance < collision_threshold:
            if self.image == self.images[0]:
                self.shield_funct()
            elif self.image == self.images[1]:
                self.plus_funct()
            elif self.image == self.images[2]:
                self.bomb_funct()
            self.kill()  # Remove the powerup sprite after collision
                



