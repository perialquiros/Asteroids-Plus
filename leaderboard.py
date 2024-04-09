import pygame
from config import *


class LeaderBoard():
    # Define file path for high scores
    
    def __init__(self):
        self.highscore_file = "highscores.txt"
        pygame.init()
        self.running = True

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
        highscores.append(score)
        highscores.sort(reverse=True) # Sort in descending order (highest first)
        highscores = highscores[:10] # Keep only the top 10 scores

        with open(self.highscore_file, "w") as file:
            for score in highscores:
                file.write(str(score) + "\n")

    def check_new_highscore(self,score):
        """Checks if the current score is a new high score"""
        highscores = self.load_highscores()
        return score > highscores[-1] if highscores else True
    
    def view(self):
        #display leaderboard
        screen.fill(BLACK)  # Clear the screen
        self.font = pygame.font.Font('Galaxus-z8Mow.ttf', 32)
        # Title text
        title_surface = self.font.render("Leaderboard", True, WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title_surface, title_rect)

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
        
        