from scratch_py import manager
import random
import os
import tests.basket as bask

def test1():

    # Folder Directory
    game_directory = os.path.split(__file__)[0]

    # Start Pygame
    game = manager.GameManager(800, 800, game_directory)
    game.change_title("Apple Catcher Game")

    # Background
    game.change_background_image("background.jpg")
    game.add_background_image("background2.png")

    # Variable
    score = 0
    speed = 10

    # Basket object
    basket = game.new_sprite('basket.png', 15)
    basket.add_costume("Logo1.png")
    basket.go_to(0,0)

    # Apple
    apple = game.new_sprite('apple.png', 5)
    apple.go_to(300,300)

    basket.say("DASD", 2)

    game.update()

    game.play_background_music("audio1.mp3")
    game.set_background_music_volume(20)

    # Game loop
    while True:
        # Check for user input
        game.get_user_events()
        
        # Check if user has quit or not
        if game.check_quit():
            break

        if basket.touch(apple):
            basket.play_sound("death.wav")
            apple.go_to(0,0)
            game.write_text("a", 30, 100, 100)
            basket.wait(2)
        
        # Move basket
        if game.key_hold("left"):
            basket.turn_right(-speed)
        if game.key_hold("right"):
            basket.turn_left(-speed)
        if game.key_hold("up"):
            basket.move(speed)
        if game.key_pressed("a"):
            basket.show_box()
        if basket.mouse_clicked():
            basket.play_sound("death.wav")

        # Show score
        game.write_text("Score: " + str(score), 30, 300, 300)

        # Update game display
        game.update()