import pygame
from sprites import *
from config import *
import sys
from ship import *

class Game:
    # set the timer for ship spawn
    spawn_timer = 0
    spawn_delay = 30
    ship_exist = False

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
        
        #take all sprites and bunch them together so we can update all at once if needed
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
        self.spawn_timer += 1

        # create the ship based on time interval
        if self.spawn_timer >= self.spawn_delay * FPS:
            self.spawn_timer = 0
            self.spawn_ship()
            self.ship_exist = True #if destroyed, changes to false
            # update ship movement

        if self.ship_exist and self.ship is not None:
            self.ship.move()

    #create background screen for game
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) #
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.display.update()

    def spawn_ship(self):
        #create the ship
        self.ship = Ships()
        self.all_sprites.add(self.ship)
        
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