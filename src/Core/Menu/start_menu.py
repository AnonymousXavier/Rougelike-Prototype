import re
import pygame
from src.UI.Button import Button
from src.Globals import settings
from src.Globals import Cache
from src.UI.label import Label

class Start_Menu:
	def __init__(self) -> None:
		cover_art_size = (settings.SCREEN_WIDTH / 4, settings.SCREEN_HEIGHT / 4)
		controls_hint_size = cover_art_size
		play_btn_size = (settings.SCREEN_WIDTH / 6, settings.SCREEN_HEIGHT / 16)
		version_label_size = (settings.SCREEN_WIDTH / 32, settings.SCREEN_HEIGHT / 32)

		title_label_size = (settings.SCREEN_WIDTH - cover_art_size[0], settings.SCREEN_HEIGHT / 7.5)
		subtile_label_size = (title_label_size[0], title_label_size[1] / 3)
		
		self.cover_art = pygame.transform.scale(Cache.Sprites.Menu.NINJA_ADVENTURE_COVER_ART, cover_art_size)
		self.controls_hint_image = pygame.transform.scale(Cache.Sprites.Menu.CONTROLS_HINT, controls_hint_size)
		self.bg_image = pygame.transform.scale(Cache.Sprites.Menu.START_MENU_BG, settings.SCREEN_SIZE)
		
		self.title_label = Label("Ninja Descent", title_label_size)	
		self.subtitle_label = Label("Made with Pygame-CE", subtile_label_size)	
		self.version_label = Label(f"v{settings.VERSION}", version_label_size)	

		self.cover_art_rect = self.cover_art.get_rect()
		self.controls_hint_image_rect = self.controls_hint_image.get_rect()

		self.play_button = Button("START", play_btn_size)

		self.position_elements()

	def position_elements(self):
		label_start_y = (self.cover_art_rect.height - (self.title_label.rect.height + self.subtitle_label.rect.height)) / 2
		self.title_label.centered = True
		self.subtitle_label.centered = True


		self.title_label.update()
		self.subtitle_label.update()
		self.version_label.update()

		self.cover_art_rect.topright = settings.SCREEN_WIDTH, 0
		self.controls_hint_image_rect.bottomright = settings.SCREEN_SIZE
		self.title_label.rect.topleft = 0,label_start_y
		self.subtitle_label.rect.topleft = self.title_label.rect.bottomleft
		self.version_label.rect.bottomleft = 0, settings.SCREEN_HEIGHT
		self.play_button.rect.center = settings.SCREEN_CENTER[0], self.controls_hint_image_rect.centery

	def draw(self, surface: pygame.Surface):
		surface.blit(self.bg_image)
		surface.blit(self.cover_art, self.cover_art_rect)
		surface.blit(self.controls_hint_image, self.controls_hint_image_rect)

		self.version_label.draw(surface)
		self.play_button.draw(surface)
		self.title_label.draw(surface)
		self.subtitle_label.draw(surface)

	def update(self):
		self.play_button.update()
