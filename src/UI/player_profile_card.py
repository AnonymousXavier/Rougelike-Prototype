import pygame
from src.Core.World import World
from src.Core.Entities.Player import Player
from src.Globals import settings, Cache
from src.UI.label import Label
from src.Misc.Save_Data import SaveData

class Player_Profile_Card:
	def __init__(self) -> None:
		fw = settings.SCREEN_WIDTH / 8
		faceset_size = (fw,fw)
		panel_size = (settings.SCREEN_CENTER[1] / 2, fw * 3)

		self.bg_image = pygame.transform.scale(Cache.Sprites.Menu.START_MENU_BG, panel_size)
		self.faceset: pygame.Surface = pygame.transform.scale(Cache.Sprites.Facesets.Green_Ninja, faceset_size)
		self.bg_image_rect = self.bg_image.get_rect()
		self.faceset_rect = self.faceset.get_rect()

		self.level_label: Label
		self.health_label: Label
		self.damage_label: Label
		self.kills_label: Label
		self.floors_label: Label

		self.position_components()

	def position_components(self):
		label_size = self.bg_image_rect.width, self.bg_image_rect.height / 12
		footer_size = self.bg_image_rect.width / 1.5, label_size[1] * 1.125
		padding = (self.bg_image_rect.height - self.faceset_rect.height ) / 6

		self.bg_image_rect.center = settings.SCREEN_CENTER
		self.faceset_rect.midtop = self.bg_image_rect.centerx, self.bg_image_rect.top + settings.SCREEN_MARGIN

		self.level_label = Label(f"Level: {SaveData.level}", label_size)
		self.health_label = Label(f"Health: {SaveData.health}", label_size)
		self.damage_label = Label(f"Damage: {SaveData.damage}", label_size)
		self.kills_label = Label(f"Kills: {SaveData.kills}", label_size)
		self.floors_label = Label(f"You Survived till Floor {SaveData.floor}", footer_size)

		self.level_label.update()
		self.health_label.update()
		self.damage_label.update()
		self.kills_label.update()
		self.floors_label.update()

		self.level_label.rect.midtop = self.faceset_rect.centerx, self.faceset_rect.bottom + padding
		self.health_label.rect.midtop = self.level_label.rect.centerx, self.level_label.rect.bottom + padding / 2
		self.damage_label.rect.midtop = self.health_label.rect.centerx, self.health_label.rect.bottom + padding / 2
		self.kills_label.rect.midtop = self.damage_label.rect.centerx, self.damage_label.rect.bottom + padding / 2

		self.floors_label.rect.center = self.kills_label.rect.centerx, self.bg_image_rect.bottom - self.floors_label.rect.height / 2 - settings.SCREEN_MARGIN

	def draw(self, surface: pygame.Surface):
		surface.blit(self.bg_image, self.bg_image_rect)
		surface.blit(self.faceset, self.faceset_rect)

		self.level_label.draw(surface)
		self.health_label.draw(surface)
		self.damage_label.draw(surface)
		self.kills_label.draw(surface)
		self.floors_label.draw(surface)
