from scratch_py import manager
import os

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Fish Catcher Game")

# Background
game.change_background_image("background1.png")

# Fish
fish = game.new_sprite('fish-a.png', 30)
fish.go_to(200, 200)

# Shark
shark = game.new_sprite('shark2-a.png', 70)
shark.add_costume('shark2-b.png')
shark.go_to(-100, -100)

# Variable
fish_speed = 13
shark_speed = 8

# Timer
start_time = game.get_timer()
end_time = start_time

while True:
    # Check for user input
    game.get_user_events()

    # Check if quit or not
    if game.check_quit():
        break

    # Move fish
    if game.key_hold("up"):
        fish.change_y(fish_speed)
    if game.key_hold("down"):
        fish.change_y(-1 * fish_speed)
    if game.key_hold("right"):
        fish.change_x(fish_speed)
    if game.key_hold("left"):
        fish.change_x(-1 * fish_speed)

    # Move shark
    if game.key_hold("w"):
        shark.change_y(shark_speed)
    if game.key_hold("s"):
        shark.change_y(-1 * shark_speed)
    if game.key_hold("d"):
        shark.change_x(shark_speed)
    if game.key_hold("a"):
        shark.change_x(-1 * shark_speed)

    # Bounce on edge
    shark.bounce_on_edge()
    fish.bounce_on_edge()

    # If shark touch fish
    if shark.touch(fish):
        shark.next_costume()
        shark.say("Yum", 2)
        shark.set_costume_after_say('shark2-a.png')
        fish.hide()
    
    # Keep Timing if 
    if fish.is_visible == True:
        end_timer = game.get_timer() - start_time

    # Write time
    game.write_text("Time: " + str(end_timer), 30, 300, 300)

    # Update game
    game.update()