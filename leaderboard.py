import pygame


class LeaderBoard():
    # Define file path for high scores
    highscore_file = "highscores.txt"

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