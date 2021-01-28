import pygame
from scratch_py.colour import *
from scratch_py.sprite import *

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
		self.background_images_lst = []
		self.background_images_dict = {}

		# Sprite object
		self.sprite_objects = []
		self.text_objects = []

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
			'space'	: pygame.K_SPACE,
			'tab'	: pygame.K_TAB,
			'return': pygame.K_RETURN,
			'0'		: pygame.K_KP0,
			'1'		: pygame.K_KP1,
			'2'		: pygame.K_KP2,
			'3'		: pygame.K_KP3,
			'4'		: pygame.K_KP4,
			'5'		: pygame.K_KP5,
			'6'		: pygame.K_KP6,
			'7'		: pygame.K_KP7,
			'8'		: pygame.K_KP8,
			'9'		: pygame.K_KP9,
			'left control': pygame.K_LCTRL,
			'right control': pygame.K_RCTRL,
		}

	# Change background
	def add_background_image(self, link):
		try:
			assert self.background_images_dict[link]
		except:
			img = pygame.image.load(self.game_directory + "\\backgrounds\\" + link).convert()
			self.background_images_dict[link] = img
			self.background_images_lst.append(link)
		
	# Rotate image [FROM STACK OVERFLOW]
	def _blit_rotate(self, sprite):

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
		origin = (sprite.x - w // 2 + min_box[0] - pivot_move[0] + w // 2, sprite.y - h // 2 - max_box[1] + pivot_move[1] + h // 2)

		# rotated image
		rotated_image = pygame.transform.rotate(sprite.image, sprite.rotation)

		# boundary box
		sprite.rect = rotated_image.get_rect()
		sprite.rect.x, sprite.rect.y = origin
		
		# display rotated image
		self.screen.blit(rotated_image, origin)

	# Change background
	def change_background_image(self, link):
		if link not in self.background_images_lst:
			img = pygame.image.load(self.game_directory + "\\backgrounds\\" + link).convert()
			self.background_images_dict[link] = img
			self.background_images_lst.append(link)
		self.current_background_image = link


	# Change game title
	def change_title(self, text):
		pygame.display.set_caption(text)

	# Check user quit
	def check_quit(self):
		for event in self.events_list:
			if event.type == pygame.QUIT: return True
		return False

	# Get background name
	def get_background_name(self):
		return self.current_background_image

	# Capture user response
	def get_user_events(self):
		self.events_list = pygame.event.get()
		self.key_pressed_list = pygame.key.get_pressed()

	def get_timer(self):
		return pygame.time.get_ticks() // 1000

	# Check if certain key is hold
	def key_hold(self, key):
		if self.key_pressed_list[self.keyboard_dict[key]]: return True
		return False

	# Check if certain key is pressed but not hold
	def key_pressed(self, key):
		for event in self.events_list:
			if event.type == pygame.KEYDOWN and event.key == self.keyboard_dict[key]: return True
		return False

	# Check if certain key is released
	def key_released(self, key):
		for event in self.events_list:
			if event.type == pygame.KEYUP and event.key == self.keyboard_dict[key]: return True
		return False

	# Next background
	def next_background_image(self):
		pos = self.background_images_lst.index(self.current_background_image)
		pos = (pos + 1) % len(self.background_images_lst)
		self.current_background_image = self.background_images_lst[pos]

	# New sprite
	def new_sprite(self, image_link, scale = 1.0):
		new_sprite = Sprite(self, image_link, scale)
		self.sprite_objects.append(new_sprite)
		return new_sprite

	# Play background music
	def play_background_music(self, link, loop_num = 0):
		self.background_sound_channel = pygame.mixer.find_channel()
		self.background_sound_channel.play(pygame.mixer.Sound(self.game_directory  + "\\sounds\\" + link), loops = loop_num)

	# Set volume
	def set_background_music_volume(self, volume):
		self.background_sound_channel.set_volume(volume / 100)

	# Stop all sounds
	def stop_all_sound(self):
		self.stop_background_music()
		for sprite in self.sprite_objects:
			if sprite.sound_channel != None:
				sprite.stop_sound()

	# Stop background music
	def stop_background_music(self):
		if self.background_sound_channel != None:
			self.background_sound_channel.stop()
		self.background_sound_channel = None

	# Start game engine
	def update(self):

		# Black background
		self.screen.fill((0,0,0))

		# Custom background
		if self.current_background_image != '':
			img = pygame.transform.scale(self.background_images_dict[self.current_background_image], (self.width, self.height))
			self.screen.blit(img, [0, 0])

		# Set up each sprite
		for sprite in self.sprite_objects:

			# Update sprite position
			sprite.update_position()

			# If not visible, continue
			if sprite.is_visible == False:
				continue

			# Update sprite rotation
			if sprite.rotation_style == 'all-around':
				self._blit_rotate(sprite)
			elif sprite.rotation_style == 'left-right':
				if sprite.rotation >= -90 and sprite.rotation <= 90:
					self.screen.blit(sprite.image, [sprite.x, sprite.y])
				else:
					self.screen.blit(pygame.transform.flip(sprite.image, True, False),[sprite.x, sprite.y])
			else:
				self.screen.blit(sprite.image, [sprite.x, sprite.y])

			# Speech bubble
			if sprite.is_say_infinite or sprite.say_cooldown > pygame.time.get_ticks():
				cloud = sprite.SpeechBubble
				cloud.render_text()
				self.screen.blit(cloud.image, [cloud.x, cloud.y])
				self.screen.blit(cloud.textFont, cloud.textRect)

			# Draw sprite center
			if sprite.box_visible == True:
				pygame.draw.circle(self.screen, RED, (sprite.x + sprite.width // 2, sprite.y + sprite.height // 2), 5)
				pygame.draw.rect(self.screen, RED, sprite.rect, 2)


		# Text Object
		for sprite in self.text_objects:
			sprite.display_text()
		self.text_objects = []

		# Display new updated position
		pygame.display.update()

		# 60 FPS
		self.clock.tick(self.fps)

	def set_fps(self, fps):
		self.fps = fps

	def write_text(self, text, font_size, x, y):
		self.text_objects.append(Text(text, font_size, x, y, self))

class Text(object):

	def __init__(self, text_str, font_size, x, y, manager) -> None:

		self.manager = manager

		# text
		font = pygame.font.Font('freesansbold.ttf', font_size)
		self.text = font.render(text_str, True, (0,0,0))

		# location
		new_x = manager.screen_width // 2 + x
		new_y = manager.screen_height // 2 - y
		self.text_rect = self.text.get_rect()
		self.text_rect.center = (new_x,new_y)

	# Display Text
	def display_text(self):
		self.manager.screen.blit(self.text, self.text_rect)
