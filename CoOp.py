import pygame
from player import *
from ship import *
from config import *
from asteroid import *
import sys
from powerups import *
import time
from leaderboard import *
import time
from PlayerCoOp import *


class CoOp:
    asteroid_timer = 0
    asteroid_spawn_delay = 1
    
    Width = WIN_WIDTH * 2
    Height = WIN_HEIGHT * 2

    def __init__(self,selected_ship):
        self.screen = pygame.display.set_mode((self.Width, self.Height))

        self.selected_ship = selected_ship

        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.Width, self.Height))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (self.Width, self.Height))
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = self.Width

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True

        #init sprite sheets
        self.asteroids = pygame.sprite.Group()

        self.powerups = pygame.sprite.Group()

        # update all variables
        self.spawn_timer_powerup = 0
        self.game_timer = 0

        
    def events(self):
        for event in pygame.event.get():
            #when you x-out of window, game quits
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
    def new(self):
        #new game
        self.playing = True
        
        #take all sprites and bunch them together so we can update all at once if needed
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

        #create player at middle of screen
        ship_image_list = SHIP_A
        if self.selected_ship == 1:
            ship_image_list = SHIP_B
        elif self.selected_ship == 2:
            ship_image_list = SHIP_C
        elif self.selected_ship == 3:
            ship_image_list = SHIP_D

        self.player1 = PlayerCoOp(self, (self.Width/TILESIZE)/2-100, (self.Height/TILESIZE)/2-100, 1, ship_image_list)
        self.player2 = PlayerCoOp(self,(self.Width/TILESIZE)/2-100, (self.Height/TILESIZE)/2-100, 2, ship_image_list)

    #create background screen for game
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        self.all_sprites.draw(self.screen) 
        for asteroid in self.asteroids:
            self.screen.blit(asteroid.image, asteroid.rect)
        self.clock.tick(FPS) #update the screen based on FPS

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
    
    def update(self):
        #game loop updates
        self.all_sprites.update()
        self.update_background()
        #self.spawn_timer_ship += 1
        self.game_timer += 1
        self.asteroid_timer += 1
        self.spawn_timer_powerup += 1
      
        #self.asteroid_alg()
               
        # check if player obtained the powerup
        for powerup in self.powerups:
            powerup.update()       

        # increase difficulty - every one minute increase difficulty and both ship and bullet time of spawn decrease by 5
        #
        #if self.game_timer >= 60 and self.spawn_delay_sp_bullet > 30:
            #add a screen display of difficult level currently - to do
        #    if self.spawn_delay_ship > 25:
        #        self.spawn_delay_ship -= 5
        #        self.spawn_delay_reg_bullet -= 5
        #    self.spawn_delay_sp_bullet -= 5
        #    self.game_timer = 0
        
        # spawn powerups based off the game time
       # if self.spawn_timer_powerup >= SPAWN_DELAY_POWERUP * FPS:
       #     powerup = Powerups(self.all_sprites, self.player)
        #    self.all_sprites.add(powerup)
        #    self.powerups.add(powerup)
        #   self.spawn_timer_powerup = 0
    
    def main(self):
        # Start the background music
        MUSIC_CHANNEL.play(BACKGROUND_MUSIC, loops=-1)

        #game loop
        self.new()
        while self.playing:
            self.events()
            self.update()
            self.draw()
                
        # Stop music before quitting
        MUSIC_CHANNEL.stop()
        self.running = False
        
        return 0
