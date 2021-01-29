#from colour import *
import pygame
import math
import random

from scratch_py.sprite import *
from scratch_py.colour import *
from scratch_py.rotation import _convert_pygame_to_scratch_rotation, _convert_scratch_to_pygame_rotation

class Sprite(pygame.sprite.Sprite):

    def __init__(self, manager, image_link, size = 100):

        # Link to game manager
        self.manager = manager

        # Load image
        self.image = pygame.image.load(self.manager.game_directory + "\\images\\" + image_link)
        self.original_image = self.image

        # Original Image Dictionary
        self.image_dict = {}
        self.image_dict[image_link] = self.image
        self.image_name = image_link

        # Adjust image size
        self.original_width, self.original_height = self.image.get_size()
        self.height = (size * self.original_height) // 100
        self.width = (size * self.original_width) // 100
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Screen resolution
        self.screen_width = self.manager.screen_width
        self.screen_height = self.manager.screen_height

        # Set image position
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        self.box_visible = False
        self.rotation = 0

        # Glide
        self.is_gliding = False
        self.x_glide_speed = 0
        self.y_glide_speed = 0

        # Velocity - Position change
        self.x_change = 0
        self.y_change = 0

        # Say
        self.is_say_infinite = False
        self.say_cooldown = 0
        self.costume_after_say = None

        # Rotation
        self.rotation_style = 'all-around' 

        # Status
        self.is_waiting = False
        self.is_visible = True

        # Sound
        self.sound_channel = None
        self.sound_volume = 100

        # Time
        self.last_response = pygame.time.get_ticks()
        self.cooldown = 0

        # Text
        self.text = ""
        self.SpeechBubble = SpeechBubble(self)

    def add_costume(self, image_link):
        image = pygame.image.load(self.manager.game_directory + "\\images\\" + image_link)
        self.image_dict[image_link] = image
        
    # If on edge, bounce
    def bounce_on_edge(self):
        # Bounce on right edge
        if self.x + self.width > self.screen_width:
            if self.rotation == 0: self.rotation = 180
            elif self.rotation < 180: self.rotation = 180 - self.rotation
            elif self.rotation > 180: self.rotation = 180 + (360 - self.rotation)
            self.x = self.screen_width - self.width

        # Bounce on left edge
        if self.x < 0:
            if self.rotation == 180: self.rotation = 0
            elif self.rotation < 180: self.rotation = 180 - self.rotation
            elif self.rotation > 180: self.rotation = 360 - (self.rotation - 180)
            self.x = 0

        # Bounce on bottom edge
        if self.y + self.height > self.screen_height:
            if self.rotation == 270: self.rotation = 90
            elif self.rotation > 270: self.rotation = 90 - (self.rotation - 270)
            elif self.rotation  < 270: self.rotation *= -1
            self.y = self.screen_height - self.height
            
        # Bounce on top edge
        elif self.y < 0:
            if self.rotation == 90: self.rotation = 270
            elif self.rotation > 90: self.rotation = 360 - self.rotation
            elif self.rotation  < 90: self.rotation *= -1
            self.y = 0

    def change_size(self, amount):
        self.size += amount
        self.height = (self.size * self.original_height) // 100
        self.width = (self.size * self.original_width) // 100
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def change_volume(self, amount):
        self.sound_volume += amount
        if self.sound_channel != None:
            self.sound_channel.set_volume(self.sound_volume)

    def change_x(self, amount):
        self.x_change = amount

    def change_y(self, amount):
        self.y_change = -1 * amount

    def clone(self):
        new = Sprite(self.manager, self.image_name, self.size)
        new.go_to(self.get_x(), self.get_y())
        new.image_dict = self.image_dict
        new.image_name = self.image_name
        new.image = self.image
        new.rotation_style = self.rotation_style
        new.rotation = self.rotation
        self.manager.sprite_objects.append(new)
        return new

    def get_costume_name(self):
        return self.image_name

    def get_costume_number(self):
        return list(self.image_dict.keys()).index(self.image_name)

    def get_direction(self):
        return _convert_pygame_to_scratch_rotation(self.rotation)

    def get_size(self):
        return self.size

    def get_volume(self):
        return self.sound_volume

    def get_x(self):
        return self.x - self.screen_width // 2 + self.width // 2

    def get_y(self):
        return self.screen_height // 2 - self.y - self.height // 2

    # Calculate glide speed
    def _glide_speed_cal(self, new_x, new_y, sec):
        self.is_gliding = True
        self.x_glide_speed = (new_x - self.x) / (sec * self.manager.fps)
        self.y_glide_speed =  (new_y - self.y) / (sec * self.manager.fps)
        self.cooldown = pygame.time.get_ticks() + (sec * 1000)

    # Glide to particular  position
    def glide(self, pos, sec):
        if self.is_gliding: return
        new_x = self.screen_width // 2 + pos[0]
        new_y =  self.screen_height // 2 - pos[1]
        self._glide_speed_cal(new_x, new_y, sec)

    def glide_to_mouse_pointer(self, sec):
        if self.is_gliding: return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self._glide_speed_cal(mouse_x, mouse_y, sec)

    def glide_to_random_position(self, sec):
        if self.is_gliding: return
        new_x = random.randint(0, self.screen_width)
        new_y =  random.randint(0, self.screen_height)
        self._glide_speed_cal(new_x, new_y, sec)

    def glide_to_sprite(self, sprite, sec):
        if self.is_gliding: return
        self._glide_speed_cal(sprite.x, sprite.y, sec)

    def go_to(self, x, y):
        self.x = self.screen_width // 2 - self.width // 2 + x
        self.y = self.screen_height // 2 - self.height // 2 - y
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2

    def go_to_random_position(self):
        self.x = random.randint(self.width // 2, self.screen_width - self.width // 2)
        self.y = random.randint(self.height // 2, self.screen_height - self.height // 2)
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2

    def hide(self):
        self.is_visible = False

    # Hide sprite box
    def hide_box(self):
        self.box_visible = False

    # Check if mouse clicked on sprite
    def mouse_clicked(self):
        for event in self.manager.events_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        return False

    # Check if Mouse hovered on Sprite
    def mouse_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def move(self, amount):
        self.x_change = amount * math.cos(math.radians(self.rotation))
        self.y_change = -1 * amount * math.sin(math.radians(self.rotation))

    def next_costume(self):
        lst = list(self.image_dict.keys())
        pos = lst.index(self.image_name)
        pos = (pos + 1) % len(lst)
        img = lst[pos]

        self.image_name = img
        self.image = self.image_dict[img]
        self.original_image = self.image
        self.original_width, self.original_height = self.image.get_size()
        self.height = (self.size * self.original_height) // 100
        self.width = (self.size * self.original_width) // 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def play_sound(self, link, loop_num = 0):
        if self.sound_channel != None and self.sound_channel.get_busy(): return
        else:
            self.sound_channel = pygame.mixer.find_channel()
            if self.sound_channel == None:
                pygame.mixer.set_num_channels(pygame.mixer.get_num_channels() + 1)
                self.sound_channel = pygame.mixer.find_channel()
            self.sound_channel.set_volume(self.sound_volume)
            self.sound_channel.play(pygame.mixer.Sound(self.manager.game_directory  + "\\sounds\\" + link), loops = loop_num)

    def point_in_direction(self, degree):
        self.rotation = degree % 360 + 90

    def point_toward_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.rotation = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    def point_toward_sprite(self, otherSprite):
        diff_x = otherSprite.x - self.x + otherSprite.width // 4
        diff_y = self.y - otherSprite.y + otherSprite.height // 4
        self.rotation = math.degrees(math.atan2(diff_y,diff_x))

    def say(self, text, sec = 0):
        self.text = text
        if sec == 0: self.is_say_infinite = True
        else: self.say_cooldown = pygame.time.get_ticks() + sec * 1000

    def set_costume_after_say(self, image_link):
        self.costume_after_say = image_link

    def set_direction(self, angle):
        self.rotation = _convert_scratch_to_pygame_rotation(angle)

    def set_rotation_style(self, rotation_style):
        self.rotation_style = rotation_style

    def set_size(self, size):
        self.size = size
        self.height = (self.size * self.original_height) // 100
        self.width = (self.size * self.original_width) // 100
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def set_volume(self, vol):
        if self.sound_channel != None:
            self.sound_channel.set_volume(vol)
        self.sound_volume = vol

    def set_x(self, amount):
        self.x = self.screen_width // 2 - self.width // 2 + amount

    def set_y(self, amount):
        self.y = self.screen_height // 2 - self.height // 2 - amount

    def stop_sound(self):
        self.sound_channel.stop()

    def show(self):
        self.is_visible = True

    # Show sprite box
    def show_box(self):
        self.box_visible = True

    def switch_costume(self, image_link):
        self.image = self.image_dict[image_link]
        self.original_image = self.image
        self.original_width, self.original_height = self.image.get_size()
        self.height = (self.size * self.original_height) // 100
        self.width = (self.size * self.original_width) // 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_name = image_link

    # Check if sprite touch other sprite
    def touch(self, other_sprite):
        if self.is_visible == False or other_sprite.is_visible == False: return False
        return pygame.sprite.collide_rect(self, other_sprite)

    def touch_edge(self):
        if self.x < self.width // 2 or self.x > self.screen_width - self.width // 2:
            return True
        elif self.y < 0 or self.y > self.screen_height - self.height // 2:
            return True
        return False

    def turn_left(self, angle):
        if not self.is_waiting: self.rotation += angle

    def turn_right(self, angle):
        if not self.is_waiting: self.rotation -= angle

    # Update position every frame
    def update_position(self):
        now = pygame.time.get_ticks()

        while self.rotation >= 360:
            self.rotation -= 360

        while self.rotation < 0:
            self.rotation += 360

        if self.is_gliding and (now <= self.cooldown):
            self.x += self.x_glide_speed
            self.y += self.y_glide_speed
            self.rect.x = self.x
            self.rect.y = self.y
        elif now > self.cooldown:
            self.x += self.x_change
            self.y += self.y_change
            self.rect.x = self.x
            self.rect.y = self.y
            self.last_response = now
            self.is_waiting = False
            self.is_gliding = False

        if self.costume_after_say != None and self.say_cooldown < pygame.time.get_ticks():
            self.switch_costume(self.costume_after_say)
            self.costume_after_say = None

        self.x_change = 0
        self.y_change = 0

        self.SpeechBubble.update_movement()

    def wait(self, sec):
        self.is_waiting = True
        self.cooldown = pygame.time.get_ticks() + (sec * 1000)

# SPEECH BUBBLE
class SpeechBubble(pygame.sprite.Sprite):

    def __init__(self, parentSprite):
        self.parentSprite = parentSprite
        self.image = pygame.image.load(self.parentSprite.manager.game_directory + "\\images\\speech.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.width = 150
        self.height = 150

    def render_text(self):
        self.textFont = self.font.render(self.parentSprite.text, True, BLACK, WHITE)
        self.textRect = self.textFont.get_rect() 
        self.textRect.center = (self.x + 80, self.y + 65)

    def update_movement(self):
        self.x = self.parentSprite.x + self.parentSprite.width
        self.y = self.parentSprite.y - self.height