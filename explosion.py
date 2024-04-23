import pygame
from config import *

class Explosion(pygame.sprite.Sprite):
        def __init__(self, position, size):
            super().__init__()
            self.images = [pygame.transform.scale(img, (size, size)) for img in EXPLOSION]  # Make sure this is defined elsewhere, e.g., in a config module
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=position)
            self.timer = pygame.time.get_ticks()

        def update(self):
            if pygame.time.get_ticks() - self.timer > 100:  # Change frame every 100 ms
                self.timer = pygame.time.get_ticks()
                self.index += 1
                if self.index >= len(self.images):
                    self.kill()
                else:
                    self.image = self.images[self.index]
                    self.rect = self.image.get_rect(center=self.rect.center)
