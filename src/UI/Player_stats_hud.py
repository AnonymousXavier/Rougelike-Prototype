import pygame
from src.UI.Button import Button
from src.UI.label import Label
from src.Core.Entities.Player import Player
from src.UI.panel import Panel
from src.Globals import settings, Cache

class Player_Stats_HUD:
	def __init__(self, player: Player):
		self.player = player

		fw, fh = settings.STATS_DISPLAY.FULL_SIZE
		self.main_panel = Panel(settings.STATS_DISPLAY.FULL_SIZE)
		self.title_label: Label
		self.subtitle_label: Label 
		self.skill_points_label: Label

		self.actual_health_label: Label
		self.actual_damage_label: Label
		self.bonus_health_label: Label
		self.bonus_damage_label: Label

		self.bonus_damage_increase_btn: Button
		self.bonus_health_increase_btn: Button
		
		self.face_set = pygame.transform.scale(Cache.Sprites.Facesets.Green_Ninja, (fw / 4, fw / 4))
		self.face_set_rect = self.face_set.get_rect()
		
		self.visible = False

		self.position_components()

	def position_components(self):
		spacing = self.main_panel.rect.height / 25
		# Recreate inventory rect
		inventory_rect = pygame.Rect(0, 0, settings.INVENTORY.FULL_SIZE[0], settings.INVENTORY.FULL_SIZE[1])
		inventory_rect.center = settings.INVENTORY.MAIN_RECT_CENTER

		# DEFINE SIZES
		disp_w, disp_h = settings.STATS_DISPLAY.FULL_SIZE
		title_label_size = (disp_w, disp_h * settings.INVENTORY.TITLE_HEIGHT_IN_PERC)
		subtitle_label_size = (disp_w, title_label_size[1] * 0.8)
		actual_stats_label_size = title_label_size[0] / 2, title_label_size[1] / 1.5
		bonus_stats_label_size = title_label_size[0] / 2, title_label_size[1] / 1.825
		upgrade_btn_size = bonus_stats_label_size[1], bonus_stats_label_size[1]


		# CREATE LABELS
		self.title_label = Label("STATS UPGRADES", title_label_size, True)
		self.subtitle_label = Label("BUFFS", title_label_size, True)
		self.skill_points_label = Label("UPGRADE POINTS", subtitle_label_size, True)
		self.actual_health_label = Label("Health", actual_stats_label_size, True)
		self.actual_damage_label = Label("Damage", actual_stats_label_size, True)
		self.bonus_health_label = Label("Extra Health", bonus_stats_label_size, True)
		self.bonus_damage_label = Label("Extra Damage", bonus_stats_label_size, True)

		# CREATE BUTTONS
		self.bonus_damage_increase_btn = Button("+", upgrade_btn_size)
		self.bonus_health_increase_btn = Button("+", upgrade_btn_size)


		# UPDATE CONSTANTS
		self.title_label.centered = True
		self.main_panel.has_border = True
		# Labels
		self.title_label.update()
		self.subtitle_label.update()
		self.actual_health_label.update()
		self.actual_damage_label.update()
		self.bonus_health_label.update()
		self.bonus_damage_label.update()
		# Buttons
		self.bonus_damage_increase_btn.bg_color = settings.Color.LIGHT_DARK_GREY
		self.bonus_health_increase_btn.bg_color = self.bonus_damage_increase_btn.bg_color
		self.bonus_damage_increase_btn.stays_down = False
		self.bonus_health_increase_btn.stays_down = False


		# POSITION COMPONENTS
		self.main_panel.border_size = settings.PANEL_BORDER_SIZE
		self.main_panel.rect.topright = inventory_rect.left - settings.SCREEN_MARGIN * 2, inventory_rect.top
		# Actual Stats
		padding = (self.face_set_rect.height - self.actual_health_label.rect.height * 2) / 4
		self.title_label.rect.topleft = self.main_panel.rect.topleft
		self.face_set_rect.topleft = spacing + self.title_label.rect.left, self.title_label.rect.bottom + spacing
		self.actual_health_label.rect.topleft = spacing + self.face_set_rect.right, self.face_set_rect.top + padding
		self.actual_damage_label.rect.topleft = self.actual_health_label.rect.left, self.actual_health_label.rect.bottom + padding * 2
		# Buff Stats
		self.subtitle_label.rect.left = spacing + self.main_panel.rect.left
		self.subtitle_label.rect.centery = self.main_panel.rect.centery
		self.bonus_health_label.rect.topleft = self.subtitle_label.rect.left, self.subtitle_label.rect.bottom + padding
		self.bonus_damage_label.rect.topleft = self.bonus_health_label.rect.left, self.bonus_health_label.rect.bottom + spacing
		# Buttons
		self.bonus_damage_increase_btn.rect.midright = self.main_panel.rect.right, self.bonus_damage_label.rect.centery
		self.bonus_health_increase_btn.rect.midright = self.bonus_damage_increase_btn.rect.right, self.bonus_health_label.rect.centery
		# Skill Points Left
		self.skill_points_label.rect.bottomleft = self.main_panel.rect.left + spacing, self.main_panel.rect.bottom - spacing

	def draw(self, surface: pygame.Surface):
		if self.visible:
			self.main_panel.draw(surface)
			self.title_label.draw(surface)
			self.subtitle_label.draw(surface)
			self.skill_points_label.draw(surface)

			self.actual_health_label.draw(surface)
			self.actual_damage_label.draw(surface)
			self.bonus_health_label.draw(surface)
			self.bonus_damage_label.draw(surface)

			if self.player.skill_points > 0:
				self.bonus_damage_increase_btn.draw(surface)
				self.bonus_health_increase_btn.draw(surface)

			surface.blit(self.face_set, self.face_set_rect)

	def update(self):
		if self.visible:
			self.actual_health_label.text = f"Health:{round(self.player.max_health)} ({round(self.player.get_max_health())})"
			self.actual_damage_label.text = f"Damage:{round(self.player.damage)} ({round(self.player.get_damage())})"
			self.bonus_health_label.text = f"Extra Health: +{round(self.player.bonus_health, 1) * 100}%"
			self.bonus_damage_label.text = f"Extra Damage: +{round(self.player.bonus_damage, 1) * 100}%"
			self.skill_points_label.text = f"Upgrade Points: {self.player.skill_points}"

			self.skill_points_label.update()
			self.title_label.update()
			self.subtitle_label.update()
			self.actual_health_label.update()
			self.actual_damage_label.update()
			self.bonus_health_label.update()
			self.bonus_damage_label.update()
			self.bonus_health_increase_btn.update()
			self.bonus_damage_increase_btn.update()

	def process_input(self, event: pygame.Event):
		if self.player.skill_points > 0:
			if self.bonus_damage_increase_btn.clicked(event):
				self.player.increase_damage_buff()
			elif self.bonus_health_increase_btn.clicked(event):
				self.player.increase_health_buff()