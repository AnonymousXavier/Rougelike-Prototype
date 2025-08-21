import pygame
from src.Globals import settings
from src.Misc import Misc
from src.UI.progress_bar import Progress_Bar
from src.UI.label import Label
from src.UI.panel import Panel
from src.Misc.UI import UI

class Enemy_Info_Display_Component(UI):
    def __init__(self, size):
        width, height = size
        
        self.section_width, self.section_height = width - settings.SCREEN_MARGIN , (height - settings.SCREEN_MARGIN) / 3
        
        super().__init__(size)

        self.section_size = (self.section_width, self.section_height)
        self.panel = Panel(size)
        self.title_label = Label("", self.section_size)
        
        self.dmg_label = Label("DMG: 1", self.section_size, False)
        
        self.health_bar = Progress_Bar(1, self.section_size)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

    def position_components(self):
        self.title_label.rect.top = self.section_height * 0.5
        self.title_label.rect.left = settings.SCREEN_MARGIN

        self.dmg_label.rect.top = self.section_height * 1.25
        self.dmg_label.rect.left = settings.SCREEN_MARGIN

        self.health_bar.rect.top = self.section_height * 2
        self.health_bar.rect.left = settings.SCREEN_MARGIN

    def update_draw_surface(self):
        self.panel.draw(self.surface)
        self.title_label.draw(self.surface)
        self.dmg_label.draw(self.surface)
        self.health_bar.draw(self.surface)

    def update(self, dt: float):
        self.position_components()
        self.title_label.update()
        self.dmg_label.update()
        self.health_bar.update(dt)

        self.update_draw_surface()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)
