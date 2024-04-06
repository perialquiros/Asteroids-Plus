import pygame
from config import *

class Button(object):

    def __init__(self, position, size, color, text, image_path=None):
        
        # image
        self.image = pygame.Surface(size)
        self.input_text = text
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, size)
        else:
            if color:
                self.image.fill(color)
            else:
                pass

        self.rect = pygame.Rect((0,0), size)
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        if text:
           
            self.text = self.font.render(self.input_text, False, WHITE)
            #text = font.render(text, False, (BLACK))
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.rect.center

            self.image.blit(self.text, self.text_rect)
        else:
            pass

        # set after centering text
        self.rect.topleft = position

    def draw(self, screen, color):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill(WHITE)
            self.text = self.font.render(self.input_text, False, BLACK)
            self.image.blit(self.text, self.text_rect)
        else:
            self.image.fill(color)
            self.text = self.font.render(self.input_text, False, WHITE)
            self.image.blit(self.text, self.text_rect)
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)