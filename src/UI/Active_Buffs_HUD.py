import pygame
from src.Core.Entities.Player import Player
from src.UI.label import Label
from src.UI.panel import Panel
from src.Globals import Cache, settings
from src.Misc.UI import UI

class BUFF_HUD(UI):
	def __init__(self, size: tuple[float, float], _id, value: str):
		super().__init__(size)
		self.icon = pygame.transform.scale(Cache.Sprites.Consumables.ALL[_id], (size[1], size[1]))
		self.icon_rect = self.icon.get_rect()
		self.label = Label(value, (self.rect.width - self.icon.width, self.rect.height))
		self.label.font_color = settings.Color.DARKER_GREY
		self.label.update()

	def update(self):
		self.icon_rect.topleft = self.rect.topleft
		self.label.rect.topright = self.rect.topright
		self.label.rect.centery = self.icon_rect.centery

	def draw(self, surface: pygame.Surface):
		surface.blit(self.icon, self.icon_rect)
		self.label.draw(surface)

class Active_Buff_HUD_Display:
	def  __init__(self, player: Player):
		self.player = player
		self.buff_huds: list[BUFF_HUD] = []

	def update(self):
		buff_hud_size = settings.SCREEN_WIDTH / 16, settings.SCREEN_HEIGHT / 32
		y = settings.SCREEN_HEIGHT - settings.SCREEN_MARGIN
		x = settings.SCREEN_WIDTH - settings.SCREEN_MARGIN
		self.buff_huds = []

		for passive_buff in self.player.passive_buffs:
			buff_hud = BUFF_HUD(buff_hud_size, passive_buff.id, str(passive_buff.duration))
			buff_hud.rect.bottomright = (x, y)
			x, y = buff_hud.rect.topright
			buff_hud.update()
			self.buff_huds.append(buff_hud)

	def draw(self, surface: pygame.Surface):
		for buff_hud in self.buff_huds:
			buff_hud.draw(surface)