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

		self.position_components()

	def position_components(self):
		title_size = settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 8

		self.title_label = Label("GAME OVER!", title_size)
		self.title_label.update()
		self.title_label.rect.center = title_size

	def draw(self, surface: pygame.Surface):
		surface.fill(settings.Color.DARKER_GREY)
		self.title_label.draw(surface)
		self.profile_card.draw(surface)

