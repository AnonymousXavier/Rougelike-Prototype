import pygame
from src.Core.Menu.start_menu import Start_Menu

class Menu:
	def __init__(self) -> None:
		self.start_menu = Start_Menu()

		self.start_game = False

	def draw_start_screen(self, surface: pygame.Surface):
		self.start_menu.draw(surface)

	def update(self):
		self.start_menu.update()
		if self.start_menu.play_button.pressed:
			self.start_game = True
