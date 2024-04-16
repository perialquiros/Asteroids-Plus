import pygame
from button import Button
import config
from button import *

class InstructionsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        # Semi-transparent background for submenu
        self.submenu_bg = pygame.Surface((600, 400))  # Smaller than the full screen
        self.submenu_bg.fill((50, 50, 50))  # Dark grey background
        self.submenu_bg.set_alpha(180)  # Semi-transparent
        self.submenu_rect = self.submenu_bg.get_rect(center=(config.WIN_WIDTH // 2, config.WIN_HEIGHT // 2))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))

        # init vars for background movement
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH

        # Define buttons
        button_y_start = 100  # Starting y-position of the first button
        self.objButton = Button((100, button_y_start), (200, 50), WHITE, 'Objectives')
        self.controlsButton = Button((100, button_y_start + 60), (200, 50), WHITE, 'Controls')
        self.mechanicsButton = Button((100, button_y_start + 120), (300, 50), WHITE, 'Gameplay Mechanics')
        self.powerupsButton = Button((100, button_y_start + 180), (200, 50), WHITE, 'Powerups')
        self.exitButton = Button((100, button_y_start + 240), (200, 50), WHITE, 'Exit')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exitButton.is_clicked(event):
                        self.running = False

            self.update_background()
            self.screen.fill((0, 0, 0))  # Clear the screen or fill with base color
            self.screen.blit(self.bg_stars, (self.bg_stars_x1, 0))
            self.screen.blit(self.bg_stars, (self.bg_stars_x2, 0))

            self.draw_transparent_overlay()  # Draw the transparent overlay

            # Draw buttons
            self.objButton.draw(self.screen, BLACK)
            self.controlsButton.draw(self.screen, BLACK)
            self.mechanicsButton.draw(self.screen, BLACK)
            self.powerupsButton.draw(self.screen, BLACK)
            self.exitButton.draw(self.screen, BLACK)

            pygame.display.update()

    def update_background(self):
        self.bg_stars_x1 -= 1  # Adjust speed as necessary
        self.bg_stars_x2 -= 1
        
        # Reset positions to loop the background
        if self.bg_stars_x1 + WIN_WIDTH < 0:
            self.bg_stars_x1 = WIN_WIDTH
            
        if self.bg_stars_x2 + WIN_WIDTH < 0:
            self.bg_stars_x2 = WIN_WIDTH
        
    def draw_transparent_overlay(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))  # Create a surface the size of the screen
        overlay.set_alpha(128)  # Set transparency: 0 is fully transparent, 255 is opaque
        overlay.fill((0, 0, 0))  # Fill with black color or any other color
        self.screen.blit(overlay, (0, 0))  # Draw the overlay on the screen

# Example usage to draw each section
    def draw_section_info(self, section):
        # Define text for each section or load from a file
        texts = {
            'Objective': "Game Objective: Survive and destroy asteroids...",
            'Controls': "Use arrow keys to move, space to shoot...",
            'Gameplay Mechanics': "Enemies appear randomly, score points...",
            'Powerups': "Collect powerups for bonuses like shields..."
        }
        text = texts.get(section, "")
        # Render text on the screen
        font = pygame.font.Font(None, 36)
        rendered_text = font.render(text, True, WHITE)
        self.screen.blit(rendered_text, (50, 350))