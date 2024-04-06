import pygame
from sprites import *
from config import *
from ship import *
from asteroid import *
import sys
from powerups import *
import time

class Game:
    # set the timer for ship spawn
    game_timer = 0
    spawn_timer_ship = 0
    spawn_delay_ship = 20
    spawn_delay_reg_bullet = 10
    spawn_delay_sp_bullet = 20

    asteroid_timer = 0
    asteroid_spawn_delay = 5
    lives = 3

    def __init__(self, selected_ship=0):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.selected_ship = selected_ship

        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True

        #init sprite sheets
        self.ships = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.ship_bullets = pygame.sprite.Group()

        self.player_bullets = pygame.sprite.Group()

        # update all variables
        self.spawn_timer_powerup = 0

        # Start the ship music
        self.ship_music_playing = False

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

        self.player = Player(self, (WIN_WIDTH/TILESIZE)/2, (WIN_HEIGHT/TILESIZE)/2, ship_image_list)
    
    def events(self):
        for event in pygame.event.get():
            #when you x-out of window, game quits
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        #game loop updates
        self.all_sprites.update()
        self.update_background()
        self.spawn_timer_ship += 1
        self.game_timer += 1
        self.asteroid_timer += 1
        self.spawn_timer_powerup += 1
        
        pygame.sprite.groupcollide(self.player_bullets, self.asteroids, True, True, pygame.sprite.collide_circle)
        
        #pygame.sprite.groupcollide(self.player_bullets, self.ships, True, True, pygame.sprite.collide_rect)
        self.asteroid_alg()

        # move the ship
        for ship in self.ships:
            ship.spawn_timer_sp_bullet += 1
            ship.spawn_timer_reg_bullet += 1
            ship.move()
            for bullet in ship.ship_sp_bullets:
                bullet.update_dir(self.player)
            ship.check_collision(self.player_bullets)

            # start shooting for regular bullet
            print(ship.spawn_timer_reg_bullet, self.spawn_delay_reg_bullet * FPS)
            if ship.spawn_timer_reg_bullet >= self.spawn_delay_reg_bullet * FPS:
                ship.shoot_reg_bullet()
                ship.spawn_timer_reg_bullet = 0
            # start shooting for special bullet
            if ship.spawn_timer_sp_bullet >= self.spawn_delay_sp_bullet * FPS:
                ship.shoot_sp_bullet()
                ship.spawn_timer_sp_bullet = 0

        # check if player obtained the powerup
        for powerup in self.powerups:
            powerup.update()

        # create the ship based on time interval
        if self.spawn_timer_ship >= self.spawn_delay_ship * FPS:
            self.spawn_timer_ship = 0
            self.spawn_ship()
            SHIP_CHANNEL.play(SHIP_MUSIC)

        # increase difficulty - every one minute increase difficulty and both ship and bullet time of spawn decrease by 5
        if self.game_timer >= 60 and self.spawn_delay_sp_bullet > 30:
            #add a screen display of difficult level currently - to do
            if self.spawn_delay_ship > 25:
                self.spawn_delay_ship -= 5
                self.spawn_delay_reg_bullet -= 5
            self.spawn_delay_sp_bullet -= 5
            self.game_timer = 0
        
        # spawn powerups based off the game time
        if self.spawn_timer_powerup >= SPAWN_DELAY_POWERUP * FPS:
            powerup = Powerups(self.all_sprites, self.player)
            self.all_sprites.add(powerup)
            self.powerups.add(powerup)
            self.spawn_timer_powerup = 0
        
    #create background screen for game
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        self.all_sprites.draw(self.screen) 
        self.clock.tick(FPS) #update the screen based on FPS

        lives_text = self.font.render('Lives: ' + str(self.player.lives), False, WHITE)
        
        # Draw the lives text
        self.screen.blit(lives_text, (10, 10))
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

    def spawn_ship(self):
        # Create a new ship and add it to the groups
        ship = Ships(self.all_sprites, self.ship_bullets)
        self.all_sprites.add(ship)
        self.ships.add(ship)
        
    def spawn_asteroid(self, size):
        asteroid = Asteroid( self, 0, 0, size)
        self.all_sprites.add(asteroid)
        self.asteroids.add(asteroid)
        
    def asteroid_alg(self):
        size = random.choice([BIG_ASTEROID_SIZE, MED_ASTEROID_SIZE, SM_ASTEROID_SIZE])

        if self.game_timer >= 30:
            self.asteroid_spawn_delay = 4
        if self.game_timer >= 60:
            self.asteroid_spawn_delay = 3

        if self.asteroid_timer >= self.asteroid_spawn_delay * FPS:
            self.spawn_asteroid(size)
            self.asteroid_timer = 0  # Reset the timer after spawning an asteroid

    def main(self):
        # Start the background music
        MUSIC_CHANNEL.play(BACKGROUND_MUSIC, loops=-1)

        #game loop
        self.new()
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.player_bullets.update()
                
        # Stop music before quitting
        MUSIC_CHANNEL.stop()
        self.running = False

