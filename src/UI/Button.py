import pygame
from src.Misc.UI import UI

class Button(UI):
	def __init__(self, text: str, size: tuple[float, float]) -> None:
		super().__init__(size)
		self.text = text = text

		self.border_size = self.rect.height / 6
		self.normal_color = self.bg_color
		self.hovered_color = self.get_hovered_color()

		self.text_surface = self.get_text_surface()
		self.text_surface_rect = self.text_surface.get_rect()

		self.pressed = False
		self.stays_down = True

	def get_hovered_color(self):
		r, g, b = self.bg_color
		return (int(r / 2), int(g / 2), int(b / 2))

	def get_text_surface(self):
		self.font_size = int(self.rect.height / 2)
		self.font = self.get_font()

		return self.font.render(self.text, True, self.font_color)

	def update(self):
		self.text_surface_rect.center = self.rect.center

		if self.stays_down:
			if not self.pressed:
				self.pressed = pygame.mouse.get_pressed()[0] and self.is_hovered()
		else:
			self.pressed = pygame.mouse.get_pressed()[0] and self.is_hovered()

	def is_hovered(self):
		return self.rect.collidepoint(pygame.mouse.get_pos())

	def clicked(self, event: pygame.Event):
		if event.type == pygame.MOUSEBUTTONUP and self.is_hovered():
			return True
		return False

	def draw(self, surface: pygame.Surface):
		color = self.bg_color if not self.is_hovered() else self.hovered_color
		pygame.draw.rect(surface, color, self.rect, 0, int(self.border_size))
		surface.blit(self.text_surface, self.text_surface_rect)