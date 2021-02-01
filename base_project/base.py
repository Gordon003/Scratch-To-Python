from scratch_py import manager
import os

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Game Title")

# Variables

# Sprites

# Game Loop
while True:

    # Check for user input
    game.get_user_events()

    # Check if quit or not
    if game.check_quit():
        break

    # Game Mechanics

    # Update game
    game.update()