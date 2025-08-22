import pygame
from src.UI.Checkbox import CheckBox
from src.UI.label import Label
from src.Globals import settings
from src.UI.panel import Panel


class Options_Menu:
	def __init__(self) -> None:
		self.visible = False
		
		self.panel: Panel = Panel(settings.OPTIONS_MENU_SIZE)
		
		self.title: Label
		self.sound_label: Label
		self.music_label: Label
		self.sprite_movement_label: Label

		self.sound_btn: CheckBox
		self.music_btn: CheckBox
		self.sprite_movement_btn: CheckBox

		self.position_components()

	def position_components(self):
		fw, fh = self.panel.rect.size
		label_size = fw, fh / 6
		options_label_size = label_size[0] / 2, label_size[1] / 1.35
		options_btn_size = (options_label_size[1], options_label_size[1])
		spacing = (fh - label_size[1]) / 4

		self.title = Label("OPTIONS", label_size)
		self.sound_label = Label("SOUND", options_label_size)
		self.music_label = Label("MUSIC", options_label_size)
		self.sprite_movement_label = Label("SPRITE GLIDING", options_label_size)

		self.sound_btn = CheckBox(options_btn_size)
		self.music_btn = CheckBox(options_btn_size)
		self.sprite_movement_btn = CheckBox(options_btn_size)

		self.sound_btn.active = True
		self.music_btn.active = True
		self.sprite_movement_btn.active = True

		self.sound_btn.update_state()
		self.music_btn.update_state()
		self.sprite_movement_btn.update_state()

		self.title.centered = True

		self.sound_label.update()
		self.music_label.update()
		self.sprite_movement_label.update()
		self.title.update()

		self.panel.rect.center = settings.SCREEN_CENTER
		self.title.rect.topleft = self.panel.rect.topleft

		margin = settings.SCREEN_MARGIN * 3
		self.sound_label.rect.topleft = self.panel.rect.left + margin, self.title.rect.bottom + spacing 
		self.music_label.rect.topleft = self.sound_label.rect.left, self.sound_label.rect.bottom + spacing / 2
		self.sprite_movement_label.rect.topleft = self.music_label.rect.left, self.music_label.rect.bottom + spacing / 2

		self.sound_btn.rect.midright = self.panel.rect.right - margin, self.sound_label.rect.centery
		self.music_btn.rect.midright = self.sound_btn.rect.right, self.music_label.rect.centery
		self.sprite_movement_btn.rect.midright = self.music_btn.rect.right, self.sprite_movement_label.rect.centery

	def draw(self, surface: pygame.Surface):
		if self.visible:
			self.panel.draw(surface)
			self.title.draw(surface)
			self.sound_label.draw(surface)
			self.music_label.draw(surface)
			self.sprite_movement_label.draw(surface)

			self.sound_btn.draw(surface)
			self.music_btn.draw(surface)
			self.sprite_movement_btn.draw(surface)

	def update(self):
		if self.visible:
			self.sound_btn.update()
			self.music_btn.update()
			self.sprite_movement_btn.update()

	def process_input(self, event):
		if self.visible:
			if self.sound_btn.clicked(event):
				settings.PLAY_SOUND = self.sound_btn.active
			if self.music_btn.clicked(event):
				settings.PLAY_MUSIC = self.music_btn.active
			if self.sprite_movement_btn.clicked(event):
				settings.SPRITE_MOVEMENT = self.sprite_movement_btn.active