import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True

        #init sprite sheets

    def new(self):
        
        #new game
        self.playing = True
        
        #take all sprites and bunch them together so we can update all aat once if needed
        self.all_sprites = pygame.sprite.LayeredUpdates()

        #create player at middle of screen
        self.player = Player(self, (WIN_WIDTH/TILESIZE)/2, (WIN_HEIGHT/TILESIZE)/2)
    
    def events(self):
        for event in pygame.event.get():
            #when you x-out of window, game quits
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        #game loop updates
        self.all_sprites.update()

    #create background screen for game
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) #
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

g = Game() #init Game class
g.new() #create a new game everytime we run
while g.running:
    g.main()

pygame.quit()
sys.exit()