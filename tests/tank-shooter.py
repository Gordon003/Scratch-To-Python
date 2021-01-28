from scratch_py import manager
import os
import random

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Fish Catcher Game")

# Background
game.change_background_image("background1.png")

# Tank
tank = game.new_sprite('tank.png', 20)
tank.point_in_direction(90)
tank.go_to(0, -250)
tank_rotation = 5

# UFO
ufo = game.new_sprite('ufo.png', 15)
ufo.go_to(random.randint(-300, 300), 300)

bullet = game.new_sprite('bullet.png', 10)
bullet.hide()
SHOOT_BULLET = False

start_time = game.get_timer()
end_time = start_time

while True:
    # Check for user input
    game.get_user_events()

    # Check if quit or not
    if game.check_quit():
        break

    # Move tank
    if game.key_hold("right"):
        tank.turn_right(tank_rotation)
    if game.key_hold("left"):
        tank.turn_left(tank_rotation)

    if game.key_pressed("x") and SHOOT_BULLET == False:
        bullet.go_to(tank.get_x(), tank.get_y())
        bullet.set_direction(tank.get_direction())
        bullet.show()

    # Write time
    game.write_text("Time: " + str(end_time), 30, 300, 300)

    # Update game
    game.update()