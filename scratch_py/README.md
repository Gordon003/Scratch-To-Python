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

Attributes
----------
width : int
  width of screen
height : int
  height of screen
game_directory: str
  path directory to game folder. os.getcwd() is sufficient.
'''

game = manager.GameManager(800, 600, os.getcwd())
```
