import pygame
from config import *
from button import *

class ShipSelection:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True
    
    def new(self):
        self.selecting = True

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)

        pygame.display.update()

    def update_background(self):
        # Move backgrounds to the left
        self.bg_stars_x1 -= 1  # Adjust speed as necessary
        self.bg_stars_x2 -= 1
        
        # If the first image is completely off-screen
        if self.bg_stars_x1 + WIN_WIDTH < 0:
            self.bg_stars_x1 = WIN_WIDTH
            
        # If the second image is completely off-screen
        if self.bg_stars_x2 + WIN_WIDTH < 0:
            self.bg_stars_x2 = WIN_WIDTH

    def main(self):
        # loop screen
        while self.running:
            self.draw()
            self.update_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False