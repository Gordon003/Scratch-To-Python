from scratch_py import manager
import os
import time

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Catch Ghost Game")

# Background
game.change_background_image('woods.png')

# Variables
ghost_score = 0

# Sprites
ghost = game.new_sprite('ghost-a.png', 70)
ghost.go_to(0,0)

# Dialogue
ghost.say("Catch me", 2)
game.update()
time.sleep(2)

time.sleep(1)
ghost.hide()
ghost_timer = game.get_timer()
ghost_appear = 2


# Game Loop
while True:

    # Check for user input
    game.get_user_events()

    # Check if quit or not
    if game.check_quit():
        break

    # Game Mechanics
    current_timer = game.get_timer()

    # Respawn new ghost
    if ghost.is_visible == False and current_timer > ghost_timer:
        ghost_timer = current_timer + ghost_appear
        ghost.go_to_random_position()
        ghost.show()
    elif ghost.is_visible == True:

        # Hide Ghost if timer expired
        if current_timer > ghost_timer:
            ghost.hide()
            ghost_timer = current_timer + 1
        # Click Ghost within time limit
        else:
            if ghost.mouse_clicked() == True:
                ghost_score += 1
                ghost.hide()

    # Game Text
    game.write_text("Score: " + str(ghost_score), 30, 300, -300)

    # Update game
    game.update()