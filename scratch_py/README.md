# Module List
| Modules    				| Links          																	|
| ------------------------- | :-------------------------------------------------------------------------------: |
| Game Manager    	| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#game-manager) 	|
| Sprite     				| [Link](https://github.com/Gordon003/Scratch-To-Python/blob/main/scratch_py/README.md#sprite) 	|

# Game Manager
The Game Manager is basically the CPU of this library. Initially started the Pygame application, it manages and updates all sprites until the user quit the application.

- Make new **Game Manager** object
```python
'''
Set up screen size 800 x 600

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
  Manager that will follow order
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
