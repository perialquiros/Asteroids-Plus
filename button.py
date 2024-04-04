import pygame
from config import *

class Button(object):

    def __init__(self, position, size, color, text, image_path=None):
        # image size
        self.image = pygame.Surface(size)
        # handle image path
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, size)
        else:
            self.image.fill(color)

        self.rect = pygame.Rect((0,0), size)
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        text = self.font.render(text, False, BLACK)
        #text = font.render(text, False, (BLACK))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        self.image.blit(text, text_rect)

        # set after centering text
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)