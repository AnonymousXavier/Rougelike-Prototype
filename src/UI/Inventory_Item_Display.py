import pygame
from src.Globals import settings
from src.UI.label import Label
from src.UI.panel import Panel


class Inventory_Item_Display:
	def __init__(self, icon: pygame.Surface, item_name: str, item_count: int) -> None:
		self.name = item_name
		self.count = item_count
		self.icon: pygame.Surface = icon

		self.panel: Panel
		self.name_label: Label
		self.count_label: Label
		self.icon_rect = icon.get_rect()

		self.surface: pygame.Surface
		self.rect = pygame.Rect()

		self.init()

	def init(self):
		fw, fh = full_size = settings.INVENTORY.ITEM_DESPLAY_WIDTH, settings.INVENTORY.ITEM_DESPLAY_HEIGHT
		sw, sh = fw / 10, fh

		name_label_size = sw * 4, sh
		count_label_size = sw*2, sh
		icons_scale = sh / self.icon.get_rect().height
		
		self.icon = pygame.transform.scale_by(self.icon, icons_scale)
		self.icon_rect = self.icon.get_rect()
		self.surface = pygame.Surface(full_size)

		self.panel = Panel(full_size)
		self.name_label = Label(self.name, name_label_size, True)
		self.count_label = Label(f"X{self.count}", count_label_size, False)

		self.panel.has_border = True
		self.name_label.centered = True
		self.count_label.centered = True

		self.panel.rect.topleft = (0, 0)
		self.icon_rect.topleft = self.rect.topleft

		self.name_label.rect.topleft = sw * 3, self.panel.rect.top
		self.count_label.rect.right = fw
		self.count_label.rect.centery = self.name_label.rect.centery

		self.rect.width = fw
		self.rect.height = fh
		self.update()

	def update(self):
		self.name_label.update()
		self.count_label.update()

	def draw(self, surface):
		self.panel.draw(self.surface)
		self.surface.blit(self.icon, self.icon_rect)
		self.name_label.draw(self.surface)
		self.count_label.draw(self.surface)

		surface.blit(self.surface, self.rect)

	def is_hovered(self, mouse_pos: tuple):
		return self.rect.collidepoint(mouse_pos)

