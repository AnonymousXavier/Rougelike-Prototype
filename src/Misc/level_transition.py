import pygame
from src.Globals import settings

class Level_Transition:
	def __init__(self):
		self.complete = False
		self.rect = self.new_rect()
		self.speed = 67

		self.finish_growing = False

	def new_rect(self):
		return pygame.Rect(settings.SCREEN_CENTER[0], settings.SCREEN_CENTER[1], 0, 0)

	def update(self, dt: float):
		w, h = self.rect.size

		if not self.finish_growing:
			w += dt * self.speed
		else:
			w -= dt * self.speed
		h = w

		self.rect.width, self.rect.height = w, h
		self.rect.center = settings.SCREEN_CENTER

		if not self.finish_growing:
			self.finish_growing = h > settings.SCREEN_WIDTH / 1.25 and w > settings.SCREEN_HEIGHT / 1.25
		self.complete = h < 0

	def draw(self, surface: pygame.Surface):
		pygame.draw.circle(surface, settings.Color.DARKER_GREY, self.rect.center, self.rect.width)

	def start(self):
		self.rect = self.new_rect()
		self.complete = False
		self.finish_growing = False