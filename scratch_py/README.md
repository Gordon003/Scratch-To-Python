# List
| Classes    				| Links          																	|
| ------------------------- | :-------------------------------------------------------------------------------: |
| Game Manager    	| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#game-manager) 	|
| Sprite     				| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#sprite) 	|

# Game Manager
The Game Manager is basically the CPU of this library. Initially started the Pygame application, it manages and updates all sprites until the user quit the application.

- Make new **Game Manager** object
```python
'''
Arguments
----------
width : int
  width of screen
height : int
  height of screen
game_directory: str
  path directory to game folder. os.getcwd() is sufficient.
  
Returns
-------
game    : GameManger
'''
from scratch_py import manager
import os

game = manager.GameManager(800, 600, os.getcwd())
```

- Add new background (But doesn't change to it)
```python
Arguments
----------
image_link : str
  name of new background
  
game.add_background_image("background1.png")
```

- Change background
```python
Arguments
----------
image_link : str
  name of new background
  
game.change_background_image("background1.png")
```

- Change game title
```python
Arguments
----------
game_title : str
  new name of game
  
game.change_title("Game Title")
```

- Change if user has quit or not
```python  
Returns
-------
result    : bool
  tell user if it has quit or not
  
result = game.check_quit()
```

- Get current background name
```python
Returns
-------
name    : str
  background's name
  
name = game.get_background_name()
```

- Get user event
```python
game.get_user_events()
```

- Get current timer
```python
Returns
-------
timer    : int
  current time
  
timer = game.get_timer()
```

- Check if certain key is hold
```python
Arguments
---------
key: str
  certain key to hold

Returns
-------
result    : bool
  tell if that key is hold or not
  
result = game.key_hold('a')
```

- Check if certain key is pressed but not hold
```python
Arguments
---------
key: str
  certain key to press

Returns
-------
result    : bool
  tell if that key is pressed or not
  
result = game.key_pressed('a')
```

- Check if certain key is released
```python
Arguments
---------
key: str
  certain key to release

Returns
-------
result    : bool
  tell if that key is released or not
  
result = game.key_released('a')
```

- Switch to next background image (similar to Scratch backdrop)
```python
game.next_background_image()
```

- Play background music
```python
Arguments
---------
link    : bool
  link to new background music
loop_num: int
  number of loops to play the new background music
  infinite if loop_num == 0
  
game.play_background_music('music.mp3', 0)
```

- Set background volume
```python
Arguments
---------
volume  : int
  new volume
  
game.set_background_music_volume(100)
```

- Stop all game and sprite sounds
```python
game.stop_all_sound()
```

- Stop background music
```python
game.stop_background_music()
```

- Update game per frame (FPS)
```python
game.update()
```

# Sprite
Sprite is basically the same Sprite from Scratch. You can move it, transform it and many more!

| Modules    				| Links          																	|
| ------------------------- | :-------------------------------------------------------------------------------: |
| Motion   	        | [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#motion) 	|
| Looks     				| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#looks) 	|
| Events     				| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#events) 	|
| Control     			| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#control) 	|
| Sensing     			| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#sensing) 	|

- Create new sprite
```python
Arguments
---------
image_link  : bool
  name of the image for the new sprite
scale       : float
  size of image
  
Returns
-------
new_sprite  : Sprite
  the new sprite
  
new_sprite = game.new_sprite("image.png", 30)
```

## Motion

- Move 10 steps
```python
sprite.move(10)
```

- Turn right 15 degrees
```python
sprite.turn_right(10)
```

- Turn left 15 degrees
```python
sprite.turn_left(10)
```

- Go to a specific position
```python
sprite.go_to(0,0)

sprite.go_to_random_position()
```

- Glide to a particular position
```python
sprite.glide(100, 100, 1)

sprite.glide_to_mouse_pointer(1)

sprite.glide_to_random_position(1)

sprite.glide_to_sprite(other_Sprite, 1)
```

- Point in direction
```python
sprite.set_direction(100)

sprite.point_toward_mouse()

sprite.point_toward_sprite(other_Sprite)
```

- Change x by 10
```python
sprite.change_x(10)
```

- Set x to 100
```python
sprite.set_x(100)
```

- Change y by 10
```python
sprite.change_y(10)
```

- Set y to 100
```python
sprite.set_y(100)
```

- If on edge, bounce
```python
sprite.bounce_on_edge()
```

- Set rotation style
```python
# All-Around, Left-Right, None
sprite.set_rotation_style("None")
```

- Get x position
```python
x = sprite.get_x()
```

- Get y position
```python
y = sprite.get_y()
```

- Get direction
```python
dir = sprite.get_direction()
```

## Looks

## Events

## Control

## Sensing

- Add new costume to sprite
```python
Arguments
---------
image_link  : str
  link to new image

- Description
```python
Arguments
----------
image_link : str
  name of new background
  
Returns
-------
result    : bool
  tell user if it has quit or not
```

- Bounce on edge (similar to Scratch function)
