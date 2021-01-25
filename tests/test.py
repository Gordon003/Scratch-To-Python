from scratch_py import manager
import os

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Fish Catcher Game")

print(os.getcwd())
# background
#game.change_background_image("background1.png")