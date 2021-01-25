import pygame
#from colour import *
from scratch_py.sprite import *
import sys
import pathlib
import os

class GameManager(object):

	# Constructor Function
	def __init__(self, width, height, game_directory):

		# Pygame core
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()

		# Game folder
		self.game_directory = game_directory

		# Frame per second
		self.fps = 60

		# Screen resolution
		self.screen_height = height
		self.screen_width = width

		# Background Image
		self.current_background_image = ''
		self.background_images_dict = {}

		# Game object
		self.sprite_objects = []
		self.text_objects = []
		self.text_rect_objects = []

		# Events
		self.key_pressed_list = []
		self.events_list = []

		# Keyboard dictionary
		self.keyboard_dict = {
			'up'	: pygame.K_UP,
			'right'	: pygame.K_RIGHT,
			'down'	: pygame.K_DOWN,
			'left'	: pygame.K_LEFT,
			'a'		: pygame.K_a,
			'b'		: pygame.K_b,
			'c'		: pygame.K_c,
			'd'		: pygame.K_d,
			'e'		: pygame.K_e,
			'f'		: pygame.K_f,
			'g'		: pygame.K_g,
			'h'		: pygame.K_h,
			'i'		: pygame.K_i,
			'j'		: pygame.K_j,
			'k'		: pygame.K_k,
			'l'		: pygame.K_l,
			'm'		: pygame.K_m,
			'n'		: pygame.K_n,
			'o'		: pygame.K_o,
			'p'		: pygame.K_p,
			'q'		: pygame.K_q,
			'r'		: pygame.K_r,
			's'		: pygame.K_s,
			't'		: pygame.K_t,
			'u'		: pygame.K_u,
			'v'		: pygame.K_v,
			'w'		: pygame.K_w,
			'x'		: pygame.K_x,
			'y'		: pygame.K_y,
			'z'		: pygame.K_z,
		}

	# Change background
	def add_background_image(self, link):

		try:
			assert self.background_images_dict[link]
		except:
			img = pygame.image.load(self.game_directory + "\\backgrounds\\" + link).convert()
			img = pygame.transform.scale(img, (self.width, self.height))
			self.background_images_dict[link] = img
		
	# Rotate Image [WAS FROM STACK OVERFLOW]
	def _blit_rotate(self, sprite):
		# blit_rotate(self, surf, image, pos, origin_pos, angle):
		# self.blit_rotate(self.screen, sprite.image, [sprite.x, sprite.y], (w//2, h//2), sprite.rotation)

		# calcaulate the axis aligned bounding box of the rotated image
		w, h       = sprite.width, sprite.height
		box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
		box_rotate = [p.rotate(sprite.rotation) for p in box]
		min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
		max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

		# calculate the translation of the pivot 
		pivot        = pygame.math.Vector2(w // 2, - h // 2)
		pivot_rotate = pivot.rotate(sprite.rotation)
		pivot_move   = pivot_rotate - pivot

		# calculate the upper left origin of the rotated image
		origin = (sprite.x- w // 2 + min_box[0] - pivot_move[0] + w // 2, sprite.y - h // 2 - max_box[1] + pivot_move[1] + h // 2)

		# rotated image
		rotated_image = pygame.transform.rotate(sprite.image, sprite.rotation)

		# boundary box
		sprite.rect = rotated_image.get_rect()
		sprite.rect.x, sprite.rect.y = origin
		
		# display rotated image
		self.screen.blit(rotated_image, origin)

	# Change background
	def change_background_image(self, link):

		try:
			assert self.background_images_dict[link]
		except:
			img = pygame.image.load(self.game_directory + "\\backgrounds\\" + link).convert()
			img = pygame.transform.scale(img, (self.width, self.height))
			self.background_images_dict[link] = img

		self.current_background_image = link


	# Change game title
	def change_title(self, text):
		pygame.display.set_caption(text)

	# Check user quit
	def check_quit(self):
		for event in self.events_list:
			if event.type == pygame.QUIT: return True
		return False

	def get_background_name(self):
		return self.current_background_image
		
	def get_background_number(self):
		return list(self.background_images_dict.keys()).index(self.current_background_image)

	# Capture user response
	def get_user_events(self):
		self.events_list = pygame.event.get()
		self.key_pressed_list = pygame.key.get_pressed()

	# Check if Certain Key is Hold
	def key_hold(self, key):
		hit = self.keyboard_dict[key]
		if self.key_pressed_list[hit]: return True
		return False

	# Check if Certain Key is Pressed
	def key_pressed(self, key):
		hit = self.keyboard_dict[key]
		for event in self.events_list:
			if event.type == pygame.KEYDOWN and event.key == hit: return True
		return False

	# Check if Certain Key is Released
	def key_released(self, key):
		hit = self.keyboard_dict[key]
		for event in self.events_list:
			if event.type == pygame.KEYUP and event.key == hit: return True
		return False

	# Change background
	def next_background_image(self):

		lst = list(self.background_images_dict.keys())
		pos = lst.index(self.current_background_image)
		pos = (pos + 1) % len(lst)
		img = lst[pos]

		self.current_background_image = img

	# New sprite
	def new_sprite(self, image_link, scale = 1.0):
		new_sprite = Sprite(self, self.game_directory, image_link, scale, self.screen_width, self.screen_height, self.fps)
		self.sprite_objects.append(new_sprite)
		return new_sprite

	# Play Background Music
	def play_background_music(self, link, loop_num = 0):
		self.background_sound_channel = pygame.mixer.find_channel()
		self.background_sound_channel.play(pygame.mixer.Sound(self.game_directory  + "\\sounds\\" + link), loops = loop_num)

	def set_background_music_volume(self, volume):
		self.background_sound_channel.set_volume(volume / 100)

	def stop_all_sound(self):
		self.stop_background_music()
		for sprite in self.sprite_objects:
			if sprite.sound_channel != None:
				sprite.stop_sound()

	def stop_background_music(self):
		if self.background_sound_channel != None:
			self.background_sound_channel.stop()
		self.background_sound_channel = None

	# Start game engine
	def update(self):

		# Black background
		self.screen.fill((0,0,0))

		# Custom background
		if self.current_background_image != '': self.screen.blit(self.background_images_dict[self.current_background_image], [0, 0])

		# Set up each sprite
		for sprite in self.sprite_objects:

			# Update sprite position
			sprite.update_position()

			# If not visible, continue
			if sprite.is_visible == False:
				continue

			# Update sprite rotation
			if sprite.rotation_style == 'all-around':
				w, h = sprite.width, sprite.height
				self._blit_rotate(sprite)
			elif sprite.rotation_style == 'left-right':
				if sprite.rotation >= -90 and sprite.rotation <= 90:
					self.screen.blit(sprite.image, [sprite.x - (sprite.width/2), sprite.y - (sprite.height/2)])
				else:
					self.screen.blit(pygame.transform.flip(sprite.image, True, False),[sprite.x - (sprite.width/2), sprite.y - (sprite.height/2)])
			else:
				self.screen.blit(sprite.image, [sprite.x - (sprite.width/2), sprite.y - (sprite.height/2)])

			# Speech Bubble
			if sprite.is_say_infinite or sprite.say_cooldown > pygame.time.get_ticks():
				cloud = sprite.SpeechBubble
				cloud.render_text()
				self.screen.blit(cloud.image, [cloud.x, cloud.y])
				self.screen.blit(cloud.textFont, cloud.textRect)

			# Draw sprite center
			if sprite.box_visible == True:
				pygame.draw.circle(self.screen, (255,0,0), (sprite.centre_x, sprite.centre_y), 5)
				pygame.draw.rect(self.screen, (255,0,0), sprite.rect, 2)


		# Text Object
		count = 0
		for sprite in self.text_objects:
			text_rect = self.text_rect_objects[count]
			self.screen.blit(sprite, text_rect)
			count += 1

		# Remove all text objects for new
		self.text_objects = []
		self.text_rect_objects = []

		# Display new updated position
		pygame.display.update()

		# 60 FPS
		self.clock.tick(self.fps)

	def set_fps(self, fps):
		self.fps = fps

	# Write Text
	def write_text(self, text, font_size, x, y):
		font = pygame.font.Font('freesansbold.ttf', font_size)
		text = font.render(text, True, (0,0,0)) 
		textRect = text.get_rect()
		new_x = self.screen_width // 2 + x
		new_y = self.screen_height // 2 - y
		textRect.center = (new_x,new_y)
		self.text_objects.append(text)
		self.text_rect_objects.append(textRect)
