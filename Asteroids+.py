import pygame
from sprites import *
from config import *
import sys
from ship import *
from asteroid import *

class Game:
    # set the timer for ship spawn
    game_timer = 0
    spawn_timer_ship = 0
    spawn_timer_reg_bullet = 0
    spawn_timer_sp_bullet = 0
    spawn_delay_ship = 30
    spawn_delay_reg_bullet = 20
    spawn_delay_sp_bullet = 60
    ship_exist = False

    asteroid_timer = 0
    asteroid_spawn_delay = 5

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True

        #init sprite sheets
        self.ship_sp_bullets = pygame.sprite.Group()
        self.ship_reg_bullets = pygame.sprite.Group()
        self.ships = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()

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

        self.spawn_timer_ship += 1
        self.spawn_timer_sp_bullet += 1
        self.spawn_timer_reg_bullet += 1
        self.game_timer += 1

        #update direction for special bullet
        for bullet in self.ship_sp_bullets:
            bullet.update_dir(self.player)
            self.spawn_sp_bullet = 0

        # move the ship
        for ship in self.ships:
            ship.move()
            
        self.asteroid_timer += 1

        if self.asteroid_timer >= self.asteroid_spawn_delay * FPS:
            self.spawn_asteroid()
            self.asteroid_timer = 0  # Reset the timer after spawning an asteroid

        # create the ship based on time interval
        if self.spawn_timer_ship >= self.spawn_delay_ship * FPS:
            self.spawn_timer_ship = 0
            self.spawn_ship()
            self.ship_exist = True #if destroyed, changes to false
        
        # start shooting for special bullet
        if self.ship_exist and self.spawn_timer_sp_bullet >= self.spawn_delay_sp_bullet * FPS:
            for ship in self.ships:
                ship.shoot_sp_bullet()
            self.spawn_timer_sp_bullet = 0
        
        # Start shooting for regular bullet
        if self.ship_exist and self.spawn_timer_reg_bullet >= self.spawn_delay_reg_bullet * FPS:
            for ship in self.ships:
                ship.shoot_reg_bullet()
            self.spawn_timer_reg_bullet = 0

        # increase difficulty - every one minute increase difficulty and both ship and bullet time of spawn decrease by 5
        if self.game_timer >= 60 and self.spawn_delay_sp_bullet > 20:
            #add a screen display of difficult level currently - to do
            if self.spawn_delay_ship > 15:
                self.spawn_delay_ship -= 5
                self.spawn_delay_reg_bullet -= 5
            self.spawn_delay_sp_bullet -= 5
            self.game_timer = 0

    #create background screen for game
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) #
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.display.update()

    def spawn_ship(self):
        # Create a new ship and add it to the groups
        ship = Ships(self.all_sprites, self.ship_sp_bullets, self.ship_reg_bullets)
        self.all_sprites.add(ship)
        self.ships.add(ship)
        
    def spawn_asteroid(self):
        asteroid = Asteroid(self, 0, 0)
        self.all_sprites.add(asteroid)
        self.asteroids.add(asteroid)

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