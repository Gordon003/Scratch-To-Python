#from colour import *
import pygame
import math
import random
import os

from scratch_py.sprite import *


class Sprite(pygame.sprite.Sprite):

    # Constructor Function
    def __init__(self, manager, game_link, image_link, scale, screen_width, screen_height, fps):

        self.manager = manager

        # Load image
        self.image = pygame.image.load(game_link + "\\images\\" + image_link)
        self.original_image = self.image

        self.game_link = game_link

        # Original Image Dictionary
        self.image_dict = {}
        self.image_dict[image_link] = self.image
        self.image_name = image_link

        # fps
        self.fps = fps

        # Adjust image size
        self.original_width, self.original_height = self.image.get_size()
        self.height = (scale * self.original_height) // 100
        self.width = (scale * self.original_width) // 100
        self.scale = scale
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        # Set image position
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.box_visible = False
        self.rotation = 0

        # image center
        self.centre_x = screen_width // 2
        self.centre_y = screen_height // 2

        # Glide
        self.is_gliding = False
        self.x_glide_speed = 0
        self.y_glide_speed = 0

        # Velocity - Position change
        self.x_change = 0
        self.y_change = 0
        
        # Screen resolution
        self.screen_width = screen_width
        self.screen_height = screen_height

        # say
        self.is_say_infinite = False
        self.say_cooldown = 0

        # Rotation
        self.rotation_style = 'all-around' 
        self.pivot = [self.width // 2, self.height // 2]

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
        image = pygame.image.load(self.game_link + "\\images\\" + image_link)
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
        self.scale += amount
        self.height = (self.scale * self.original_height) // 100
        self.width = (self.scale * self.original_width) // 100
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def change_volume(self, amount):
        self.sound_volume += amount
        if self.sound_channel != None:
            self.sound_channel.set_volume(self.sound_volume)

    # Change X
    def change_x(self, amount):
        self.x_change = amount

    # Change Y
    def change_y(self, amount):
        self.y_change = -1 * amount

    def get_costume_name(self):
        return self.image_name

    def get_costume_number(self):
        return list(self.image_dict.keys()).index(self.image_name)

    # Get Direction
    def get_direction(self):
        if self.rotation == 0: return 90
        elif self.rotation == 90: return 0
        elif self.rotation == 180: return -90
        elif self.rotation == 270: return 180
        elif self.rotation > 0 and self.rotation < 90: return 90 - self.rotation
        elif self.rotation > 90 and self.rotation < 180: return -1 * (self.rotation - 90)
        elif self.rotation > 180 and self.rotation < 270: return 180 + (self.rotation - 270)
        elif self.rotation > 270 and self.rotation < 360: return 180 - (self.rotation - 270)

    def get_size(self):
        return self.scale

    def get_volume(self):
        return self.sound_volume

    # Get X
    def get_x(self):
        return self.centre_x - self.screen_width // 2

	# Get Y
    def get_y(self):
        return self.screen_height // 2 - self.centre_y

    def _glide_speed_cal(self, new_x, new_y, sec):
        self.is_gliding = True
        self.x_glide_speed = (new_x - self.centre_x) / (sec * self.fps)
        self.y_glide_speed =  (new_y - self.centre_y) / (sec * self.fps)
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

    # Glide to random position
    def glide_to_random_position(self, sec):
        if self.is_gliding: return
        new_x = random.randint(0, self.screen_width)
        new_y =  random.randint(0, self.screen_height)
        self._glide_speed_cal(new_x, new_y, sec)

    # Glide to random position
    def glide_to_sprite(self, sprite, sec):
        if self.is_gliding: return
        self._glide_speed_cal(sprite.centre_x, sprite.centre_y, sec)

    # Go to specific position
    def go_to(self, x, y):
        self.x = self.screen_width // 2 - self.width // 2 + x
        self.y = self.screen_height // 2 - self.height // 2 - y

    # Go to random position
    def go_to_random_position(self):
        self.x = random.randint(self.width // 2, self.screen_width - self.width // 2)
        self.y = random.randint(self.height // 2, self.screen_height - self.height // 2)


    def hide(self):
        self.is_visible = False

    def hide_box(self):
        self.box_visible = False

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

    # Move sprite
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
        self.height = (self.scale * self.original_height) // 100
        self.width = (self.scale * self.original_width) // 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def play_sound(self, link, loop_num = 0):
        if self.sound_channel != None and self.sound_channel.get_busy():
            return
        else:
            self.sound_channel = pygame.mixer.find_channel()
            if self.sound_channel == None:
                pygame.mixer.set_num_channels(pygame.mixer.get_num_channels() + 1)
                self.sound_channel = pygame.mixer.find_channel()
            self.sound_channel.set_volume(self.sound_volume)

            self.sound_channel.play(pygame.mixer.Sound(self.game_link  + "\\sounds\\" + link), loops = loop_num)

    # Point in specific location
    def point_in_direction(self, degree):
        self.rotation = degree % 360

    	# Point toward Mouse
    def point_toward_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.centre_x, mouse_y - self.centre_y
        self.rotation = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    # Point toward Sprite
    def point_toward_sprite(self, otherSprite):
        diff_x = otherSprite.centre_x - self.centre_x
        diff_y = self.centre_y - otherSprite.centre_y
        self.rotation = math.degrees(math.atan2(diff_y,diff_x))

    # Say
    def say(self, text, sec = 0):
        self.text = text

        if sec == 0:
            self.is_say_infinite = True
        else:
            self.say_cooldown = pygame.time.get_ticks() + sec * 1000

    # Set Direction
    def set_direction(self, angle):
        self.rotation = 90 - angle

    # Set Rotation
    def set_rotation_style(self, rotation_style):
        self.rotation_style = rotation_style

    def set_scale(self, scale):
        self.scale = scale
        self.height = (self.scale * self.original_height) // 100
        self.width = (self.scale * self.original_width) // 100
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    # Set size
    def set_size(self, scale):
        self.scale = scale
        self.height = int(scale * self.original_height // 100)
        self.width = int(scale * self.original_width // 100)

    def set_volume(self, vol):
        if self.sound_channel != None:
            self.sound_channel.set_volume(vol)
        self.sound_volume = vol

    # Set X position
    def set_x(self, amount):
        self.x = self.screen_width // 2 - self.width // 2 + amount

	# Set Y position
    def set_y(self, amount):
        self.y = self.screen_height // 2 - self.height // 2 - amount

    def stop_sound(self):
        self.sound_channel.stop()

    def show(self):
        self.is_visible = True

    def show_box(self):
        self.box_visible = True

    def switch_costume(self, image_link):
        self.image = self.image_dict[image_link]
        self.original_image = self.image
        self.original_width, self.original_height = self.image.get_size()
        self.height = (self.scale * self.original_height) // 100
        self.width = (self.scale * self.original_width) // 100
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_name = image_link

    # Check if sprite touch other sprite
    def touch(self, other_sprite):
        return pygame.sprite.collide_rect(self, other_sprite)

    # Turn Left
    def turn_left(self, angle):
        if not self.is_waiting:
            self.rotation += angle

    # Turn Right
    def turn_right(self, angle):
        if not self.is_waiting:
            self.rotation -= angle

    # Update position every frame
    def update_position(self):

        now = pygame.time.get_ticks()

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

        self.centre_x = self.x + self.width // 2
        self.centre_y = self.y + self.height // 2

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
        self.image = pygame.image.load(self.parentSprite.game_link  + "\\images\\speech.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.width = 150
        self.height = 150

    def render_text(self):
        self.textFont = self.font.render(self.parentSprite.text, True, (255,255,255), (0,0,0))
        self.textRect = self.textFont.get_rect() 
        self.textRect.center = (self.x + 80, self.y + 65)

    def update_movement(self):
        self.x = self.parentSprite.x + self.parentSprite.width
        self.y = self.parentSprite.y - self.height