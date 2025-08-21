import pygame
from src.UI.Description_Label import Desciption_Label
from src.Globals import settings
from src.Core.Entities.Player import Player
from src.Misc.UI import UI
from src.UI.Inventory_Item_Display import Inventory_Item_Display


class Inventory_Items_Container(UI):
	def __init__(self, size: tuple[float, float], player: Player):
		super().__init__(size)

		self.player = player
		self.items: list[UI] = []
		self.drawn_inventory_items: list[Inventory_Item_Display] = []

		self.surface = pygame.Surface(size, pygame.SRCALPHA)
		self.hovered_item_display: Inventory_Item_Display = None
		self.description_label: Desciption_Label = None

	def inventory_items(self):
		items_lists = []
		h = settings.INVENTORY.ITEM_DESPLAY_HEIGHT
		for i, item_name in enumerate(self.player.inventory.items):
			generic_item = self.player.inventory.items[item_name][0]
			inventory_item_display = Inventory_Item_Display(generic_item.get_image(), item_name, len(self.player.inventory.items[item_name]))

			inventory_item_display.rect.top = i * h
			inventory_item_display.rect.left = settings.SCREEN_MARGIN
			items_lists.append(inventory_item_display)

		for inventory_item_display in items_lists:
			inventory_item_display.draw(self.surface)

		self.drawn_inventory_items = items_lists

	def update(self, dt: float):
		if self.hovered_item_display:
			self.position_description_label()

	def position_description_label(self):
		cx, cy = self.rect.center
		ox, oy = self.rect.topleft
		chx, chy = self.hovered_item_display.rect.center

		if cx > chx:
			self.description_label.rect.top = self.hovered_item_display.rect.top + oy
			self.description_label.rect.left = self.hovered_item_display.rect.right + ox
		else:
			self.description_label.rect.top = self.hovered_item_display.rect.top + oy
			self.description_label.rect.right = self.hovered_item_display.rect.left + ox

	def create_description_label(self):
		item_list = self.player.inventory.items[self.hovered_item_display.name_label.text]
		font_size = int(self.hovered_item_display.icon_rect.height / 2.25)
		item = item_list[0]

		return Desciption_Label(item.description, font_size)

	def get_hovered_item(self):
		actual_mx, actual_my = pygame.mouse.get_pos()
		tx, ty = self.rect.topleft
		mx, my = actual_mx - tx, actual_my - ty
		sw, sh = self.surface.get_size()

		if mx <= 0 or my <= 0 or mx > sw or my > sh:
			return

		for item in self.drawn_inventory_items:
			if item.is_hovered((mx, my)):
				return item
		
		return None

	def refresh(self):
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.inventory_items()

	def draw(self, surface: pygame.Surface):
		surface.blit(self.surface, self.rect)
		if self.hovered_item_display:
			self.description_label.draw(surface)

	def process_input(self, event: pygame.Event):
		if event.type == pygame.MOUSEMOTION:
			self.hovered_item_display = self.get_hovered_item()
			if self.hovered_item_display:
				self.description_label = self.create_description_label()
			else:
				self.description_label = None
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if self.hovered_item_display:
				consumable_list = self.player.inventory.items[self.hovered_item_display.name_label.text]
				if len(consumable_list) > 0:
					consumable_item = consumable_list[0]
					if self.player.inventory.remove(consumable_item):
						consumable_item.use(self.player)
					self.hovered_item_display = None
					self.description_label = None

					self.refresh()



