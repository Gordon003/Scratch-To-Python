# Module List
| Modules    				| Links          																	|
| ------------------------- | :-------------------------------------------------------------------------------: |
| Game Manager    	| [Link](https://github.com/Gordon003/Scratch-To-Python#game-manager) 	|
| Sprite     				| [Link](here) 	|

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
  
game.check_quit()
```

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
