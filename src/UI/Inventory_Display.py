import pygame
from src.UI.Inventory_Items_Container import Inventory_Items_Container
from src.Core.Entities.Player import Player
from src.Globals import settings
from src.UI.label import Label
from src.UI.panel import Panel

class Inventory_Display:
	def __init__(self, player: Player):
		self.player = player
		self.main_panel = Panel(settings.INVENTORY.FULL_SIZE)
		self.title_label: Label
		self.inventory_display_container = Inventory_Items_Container(settings.INVENTORY.DISPLAY_SIZE, player)
		
		self.visible = False
		self.frames_display_has_been_visible = 0

		self.init()

	def init(self):
		inv_w, inv_h = settings.INVENTORY.DISPLAY_SIZE
		# Using Display Size as Height, to add a space between the title and 
		# Actual Height is the height if the display size wasnt used
		title_label_size = (inv_w, inv_h * settings.INVENTORY.TITLE_HEIGHT_IN_PERC)
		actual_title_height = settings.INVENTORY.TITLE_HEIGHT_IN_PERC * settings.INVENTORY.FULL_SIZE[1]

		self.title_label = Label("INVENTORY", title_label_size, True)

		# Update Constants
		self.title_label.centered = True
		self.main_panel.has_border = True

		self.main_panel.border_size = settings.PANEL_BORDER_SIZE

		self.title_label.update()

		# Position Components
		self.main_panel.rect.center = settings.INVENTORY.MAIN_RECT_CENTER

		self.inventory_display_container.rect.centerx = self.main_panel.rect.centerx
		self.inventory_display_container.rect.centery = self.main_panel.rect.centery + actual_title_height / 2
		self.title_label.rect.topleft = self.main_panel.rect.topleft


	def update(self, dt: float):
		if self.visible:
			if self.frames_display_has_been_visible == 0:
				self.inventory_display_container.refresh()
			self.frames_display_has_been_visible += 1
			self.inventory_display_container.update(dt)

	def draw(self, surface: pygame.Surface):
		if self.visible:
			self.main_panel.draw(surface)
			self.title_label.draw(surface)

			self.inventory_display_container.draw(surface)
		else:
			self.frames_display_has_been_visible = 0

	def process_input(self, event: pygame.Event):
		if self.visible:
			self.inventory_display_container.process_input(event)