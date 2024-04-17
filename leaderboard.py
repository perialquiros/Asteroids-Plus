import pygame
from config import *
from button import *

class LeaderBoard():
    # Define file path for high scores
    
    def __init__(self):
        self.highscore_file = "highscores.txt"
        pygame.init()
        self.running = True
        self.back_Button = Button((WIN_WIDTH/2 - 75, WIN_HEIGHT/2 + 150), (150, 100), WHITE, "BACK")
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        self.background = pygame.image.load('Images/backgrounds/space-backgound.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIN_WIDTH, WIN_HEIGHT))
        stars_image = pygame.image.load('Images/backgrounds/space-stars.png')
        self.bg_stars = pygame.transform.scale(stars_image, (WIN_WIDTH, WIN_HEIGHT))
        self.bg_stars_x1 = 0
        self.bg_stars_x2 = WIN_WIDTH

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)


    def load_highscores(self):
        """Loads high scores from the file"""
        try:
            with open(self.highscore_file, "r") as file:
                scores = [int(line.strip()) for line in file.readlines()]
            return scores[:10] # Return only the top 10 scores
        except FileNotFoundError:
            # Create an empty file if it doesn't exist
            with open(self.highscore_file, "w") as file:
                pass
            return []

    def save_highscore(self,score):
        """Saves a new high score to the file"""
        highscores = self.load_highscores()
        if(score == 0):
            return
        highscores.append(score)
        highscores.sort(reverse=True) # Sort in descending order (highest first)
        highscores = highscores[:10] # Keep only the top 10 scores

        with open(self.highscore_file, "w") as file:
            for score in highscores:
                file.write(str(score) + "\n")

    def check_new_highscore(self,score):
        """Checks if the current score is a new high score"""
        if(score == 0):
            return False
        highscores = self.load_highscores()
        if score == highscores[0]:
            return True
        return False    
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x1 ,0))
        self.screen.blit(self.bg_stars, (self.bg_stars_x2 ,0))
        
        self.clock.tick(FPS) #update the screen based on FPS
        pygame.mouse.set_visible(True)
        
        self.back_Button.draw(self.screen, BLACK)
        
        title_surface = self.font.render("Leaderboard", True, WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 50))
        
        points_surface = self.font.render("Points", True, WHITE)
        points_rect = points_surface.get_rect(center=(screen.get_width() // 2 + 350, 80))
        screen.blit(title_surface, title_rect)
        screen.blit(points_surface, points_rect)


        # Leaderboard entries
        y_pos = 100
        count = 1
        for score in self.load_highscores():
            rank_text = self.font.render(f"{count}.", True, WHITE)
            #name_text = self.font.render(name, True, WHITE)
            score_text = self.font.render(str(score), True, WHITE)

            rank_rect = rank_text.get_rect(y=y_pos, x=20)
            #name_rect = name_text.get_rect(y=y_pos, x=60)
            score_rect = score_text.get_rect(y=y_pos, x=screen.get_width() - score_text.get_width() - 20)

            screen.blit(rank_text, rank_rect)
            #screen.blit(name_text, name_rect)
            screen.blit(score_text, score_rect)

            y_pos += 30  # Adjust spacing between entries
            count +=1 #adjust rank

        # Update the display
        pygame.display.flip()
        
        
        pygame.display.update()
    
    def updateBackground(self):
         # Move backgrounds to the left
        self.bg_stars_x1 -= 1  # Adjust speed as necessary
        self.bg_stars_x2 -= 1
        
        # If the first image is completely off-screen
        if self.bg_stars_x1 + WIN_WIDTH < 0:
            self.bg_stars_x1 = WIN_WIDTH
            
        # If the second image is completely off-screen
        if self.bg_stars_x2 + WIN_WIDTH < 0:
            self.bg_stars_x2 = WIN_WIDTH
            
    def view(self):
        #display leaderboard
        while(self.running):
            self.draw()
            self.updateBackground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if self.back_Button.is_clicked(event):
                    self.running = False
       
        