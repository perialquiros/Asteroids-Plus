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

        self.animate_loop = 0 # control animation speed
        self.frame = 0 # frame of animation
        self.selection = 0 # default - ship A
        #self.ship = SHIP_A_BUTTON # default

        self.next_Button = Button((WIN_WIDTH/2 + 100, WIN_HEIGHT/2 + 150), (100, 100), WHITE, "NEXT")
        self.prev_Button = Button((WIN_WIDTH/2 - 200, WIN_HEIGHT/2 + 150), (100, 100), WHITE, "PREV")
        self.select_Button = Button((WIN_WIDTH/2 - 75, WIN_HEIGHT/2 + 150), (150, 100), WHITE, "SELECT")
    def new(self):
        self.selecting = True

    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)


        if self.selection == 0:
            self.screen.blit(SHIP_A_BUTTON[self.frame], (WIN_WIDTH/2 - 100 ,WIN_HEIGHT/2 - 150))
           
        elif self.selection == 1:
            self.screen.blit(SHIP_B_BUTTON[self.frame], (WIN_WIDTH/2 - 100 ,WIN_HEIGHT/2 - 150))
            
        elif self.selection == 2:
            self.screen.blit(SHIP_C_BUTTON[self.frame], (WIN_WIDTH/2 - 100 ,WIN_HEIGHT/2 - 150))
       
        elif self.selection == 3:
            self.screen.blit(SHIP_D_BUTTON[self.frame], (WIN_WIDTH/2 - 100 ,WIN_HEIGHT/2 - 150))
            
        self.next_Button.draw(self.screen, BLACK)
        self.prev_Button.draw(self.screen, BLACK)
        self.select_Button.draw(self.screen, BLACK)

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

    def animate_ship(self):
        if self.animate_loop >= 7:
                self.animate_loop = 0
                if self.frame >= 2:
                    self.frame = 0
                else:
                    self.frame += 1
        else:
            self.animate_loop += 1

    def main(self):
        # loop screen
        while self.running:
            self.animate_ship()
            self.draw()
            self.update_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if self.next_Button.is_clicked(event):
                    self.selection += 1

                    if self.selection == 4:
                        self.selection = 0

                if self.prev_Button.is_clicked(event):
                    self.selection -= 1
                    
                    if self.selection == -1:
                        self.selection = 3

                if self.select_Button.is_clicked(event):
                    self.running = False
                    return self.selection 

            