import pygame
from sprites import *
from ship import *
from asteroid import *
import sys
import config

class Game:
    asteroid_timer = 0
    asteroid_spawn_delay = 5
    lives = 3

    def __init__(self):
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        self.running = True

        #init sprite sheets
        self.ship_sp_bullets = pygame.sprite.Group()
        self.ship_reg_bullets = pygame.sprite.Group()
        self.ships = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()

    def new(self):
        
        #new game
        self.playing = True
        
        #take all sprites and bunch them together so we can update all at once if needed
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()

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

        config.SPAWN_TIMER_SHIP += 1
        config.SPAWN_TIMER_SP_BULLET += 1
        config.SPAWN_TIMER_REG_BULLET += 1
        config.GAME_TIMER += 1
        self.asteroid_timer += 1
        
        self.asteroid_alg()

        #update direction for special bullet
        for bullet in self.ship_sp_bullets:
            bullet.update_dir(self.player)

        # move the ship
        for ship in self.ships:
            ship.move()

        # create the ship based on time interval
        if config.SPAWN_TIMER_SHIP >= config.SPAWN_DELAY_SHIP * FPS:
            config.SPAWN_TIMER_SHIP = 0
            self.spawn_ship()
            config.SHIP_EXIST = True #if destroyed, changes to false
        
        # start shooting for special bullet
        if config.SHIP_EXIST and config.SPAWN_TIMER_SP_BULLET >= config.SPAWN_DELAY_SP_BULLET * FPS:
            for ship in self.ships:
                ship.shoot_sp_bullet()
            config.SPAWN_TIMER_SP_BULLET = 0
        
        # Start shooting for regular bullet
        if config.SHIP_EXIST and config.SPAWN_TIMER_REG_BULLET >= config.SPAWN_DELAY_REG_BULLET * FPS:
            for ship in self.ships:
                ship.shoot_reg_bullet()
            config.SPAWN_TIMER_REG_BULLET = 0

        # increase difficulty - every one minute increase difficulty and both ship and bullet time of spawn decrease by 5
        if config.GAME_TIMER >= 60 and config.SPAWN_DELAY_SP_BULLET > 30:
            #add a screen display of difficult level currently - to do
            if config.SPAWN_DELAY_SHIP > 25:
                config.SPAWN_DELAY_SHIP -= 5
                config.SPAWN_DELAY_REG_BULLET -= 5
            config.SPAWN_DELAY_SP_BULLET -= 5
            config.GAME_TIMER = 0
        
    #create background screen for game
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen) #
        self.clock.tick(FPS) #update the screen based on FPS

        lives_text = self.font.render('Lives: ' + str(self.player.lives), False, BLACK)
        
        # Draw the lives text
        self.screen.blit(lives_text, (10, 10))
        pygame.display.update()

    def spawn_ship(self):
        # Create a new ship and add it to the groups
        ship = Ships(self.all_sprites, self.ship_sp_bullets, self.ship_reg_bullets)
        self.all_sprites.add(ship)
        self.ships.add(ship)
        
    def spawn_asteroid(self, size):
        asteroid = Asteroid( self, 0, 0, size)
        self.all_sprites.add(asteroid)
        self.asteroids.add(asteroid)
        
    def asteroid_alg(self):
        size = random.choice([BIG_ASTEROID_SIZE, MED_ASTEROID_SIZE, SM_ASTEROID_SIZE])

        if config.GAME_TIMER >= 30:
            self.asteroid_spawn_delay = 4
        if config.GAME_TIMER >= 60:
            self.asteroid_spawn_delay = 3

        if self.asteroid_timer >= self.asteroid_spawn_delay * FPS:
            self.spawn_asteroid(size)
            self.asteroid_timer = 0  # Reset the timer after spawning an asteroid

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()

        self.running = False

