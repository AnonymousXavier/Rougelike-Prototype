import pygame
from src.Globals import settings
from src.Misc.UI import UI

class CheckBox(UI):
	def __init__(self, size: tuple[float, float]):
		super().__init__(size)

		self.text = "OFF"
		self.active = False
		self.border_size = size[1] * 0.3
		self.pressed = False

		self.hovered_color = self.get_hovered_color()
		self.text_surface = self.get_text_surface()

	def update(self):
		pass

	def get_hovered_color(self):
		return settings.Color.LIGHT_DARK_GREY

	def get_text_surface(self):
		self.font_size = int(self.rect.height / 2)
		self.font = self.get_font()

		font_color = "red" if self.text == "OFF" else "green"
		return self.font.render(self.text, True, font_color)

	def update_state(self):
		if self.pressed:
			self.active = not self.active
		self.text = "ON" if self.active else "OFF"
		self.text_surface = self.get_text_surface()

	def draw(self, surface: pygame.Surface):
		color = self.bg_color if not self.is_hovered() else self.hovered_color
		pygame.draw.rect(surface, color, self.rect, 0, int(self.border_size))
		surface.blit(self.text_surface, self.text_surface.get_rect(center=self.rect.center))

	def is_hovered(self):
		return self.rect.collidepoint(pygame.mouse.get_pos())

	def clicked(self, event: pygame.Event):
		if event.type == pygame.MOUSEBUTTONUP and self.is_hovered():
			self.pressed = True
			self.update_state()
			return True
		self.pressed = False
		self.update_state()
		return False