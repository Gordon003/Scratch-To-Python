from scratch_py import manager
import os
import random
import time

# Start Pygame
game = manager.GameManager(800, 800, os.getcwd())
game.change_title("Tank Shooter Game")

# Background
game.change_background_image("background1.png")

# Tank
tank = game.new_sprite('tank.png', 20)
tank.go_to(0, -250)
tank_rotation = 5
tank.set_direction(0)
tank_score = 0

# UFO
ufo = game.new_sprite('ufo.png', 15)
ufo.set_rotation_style("None")
ufo.go_to(random.randint(-300, 300), 300)

ufo_list = [ufo, ufo.clone()]
ufo_speed = 1

for ufo in ufo_list:
    ufo.go_to(random.randint(-300, 300), 300)

# Bullet
bullet = game.new_sprite('bullet.png', 10)
bullet.hide()
SHOOT_BULLET = False
bullet_speed = 15

# Timer
start_time = game.get_timer()
end_time = start_time

# Level
level = 1

GAME_OVER = False

while not GAME_OVER:
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

    # Tank shoot
    if game.key_pressed("space") and SHOOT_BULLET == False:
        bullet.go_to(tank.get_x(), tank.get_y())
        bullet.set_direction(tank.get_direction())
        bullet.show()
        SHOOT_BULLET = True

    # Bullet's moving
    if SHOOT_BULLET == True:
        bullet.move(bullet_speed)
        if bullet.touch_edge() == True:
            bullet.hide()
            bullet.go_to(-500, -500)
            SHOOT_BULLET = False

    # UFO
    for ufo in ufo_list:
        if SHOOT_BULLET == True and bullet.touch(ufo) == True:
            ufo.go_to(random.randint(-300, 300), 300) 
            bullet.go_to(-500, -500)
            bullet.hide()
            SHOOT_BULLET = False
            tank_score += 1
        else:
            ufo.point_toward_sprite(tank)
            ufo.move(ufo_speed)

        if ufo.touch(tank):
            GAME_OVER = True

    # Increase UFO speed
    if level == 1 and tank_score > 5:
        ufo_speed += 2
        level += 1
    elif level == 2 and tank_score > 10:
        ufo_list.append(ufo.clone())
        level += 1

    # Timer
    end_time = game.get_timer()

    # Write time
    game.write_text("Score: " + str(tank_score), 30, 300, 300)

    # Update game
    game.update()

game.write_text("Time: " + str(end_time) + " seconds", 30, 0, 0)
game.write_text("Score: " + str(tank_score), 30, 300, 300)
game.update()
time.sleep(3)