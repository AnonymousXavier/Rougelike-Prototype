import pygame
from src.Globals import settings
from src.Misc import Misc


class Desciption_Label:
	def __init__(self, text: str, font_size: float) -> None:
		self.max_text_string_lenght = settings.DESCRIPTION_MAX_WRAP_LENGHT
		self.max_test_width = font_size * self.max_text_string_lenght
		self.font_size = font_size
		self.text = text
		self.bold = True

		self.text_surface = self.create_text_surface()
		self.rect = self.text_surface.get_rect()

	def get_font(self):
		return Misc.get_font(settings.Font_Names.HUD, self.font_size, is_bold=self.bold, is_italic=False)

	def create_text_surface(self):
		wrapped_text = Misc.wrap_text(self.text, self.max_text_string_lenght)
		font = self.get_font()

		surface = pygame.Surface((self.max_text_string_lenght * self.font_size,  len(wrapped_text) * self.font_size), pygame.SRCALPHA)
		
		h = self.font_size
		for i, word in enumerate(wrapped_text):
			text_surface = font.render(word, True, settings.Color.OFF_WHITE)
			text_surface_rect = text_surface.get_rect(topleft=(0, h * i))
			surface.blit(text_surface, text_surface_rect)

		return surface

	def update(self):
		old_center = self.rect.center
		self.text_surface = self.create_text_surface()
		self.rect = self.text_surface.get_rect(center=old_center)

	def draw(self, surface: pygame.Surface):
		surface.blit(self.text_surface, self.rect)





