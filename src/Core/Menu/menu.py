import pygame
from src.Core.World import World
from src.Core.Menu.game_over import End_Menu
from src.Core.Menu.start_menu import Start_Menu

class Menu:
	def __init__(self, world: World) -> None:
		self.start_menu = Start_Menu()
		self.game_over = End_Menu(world)
		self.start_game = False

	def draw_start_screen(self, surface: pygame.Surface):
		self.start_menu.draw(surface)

	def draw_end_menu(self, surface: pygame.Surface):
		self.game_over.draw(surface)

	def update(self):
		self.start_menu.update()
		if self.start_menu.play_button.pressed:
			self.start_game = True
