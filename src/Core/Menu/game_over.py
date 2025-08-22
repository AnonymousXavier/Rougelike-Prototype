import pygame
from src.UI.player_profile_card import Player_Profile_Card
from src.Core.World import World
from src.Core.Entities.Player import Player
from src.UI.Button import Button
from src.Globals import settings, Cache
from src.UI.label import Label

class End_Menu:
	def __init__(self, world: World) -> None:

		self.profile_card = Player_Profile_Card()
		self.title_label: Label
		self.menu_btn: Button
		self.return_to_menu = False

		self.position_components()

	def position_components(self):
		title_size = settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 8
		menu_btn_size = settings.SCREEN_WIDTH / 3, settings.SCREEN_HEIGHT / 16 

		self.title_label = Label("GAME OVER!", title_size)

		self.menu_btn = Button("Return To Menu", menu_btn_size)

		self.title_label.update()
		self.title_label.rect.center = title_size
		self.menu_btn.rect.center = settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT * 0.9
		self.menu_btn.update()

	def draw(self, surface: pygame.Surface):
		surface.fill(settings.Color.DARKER_GREY)
		self.title_label.draw(surface)
		self.profile_card.draw(surface)
		self.menu_btn.draw(surface)

	def update(self):
		self.menu_btn.update()

