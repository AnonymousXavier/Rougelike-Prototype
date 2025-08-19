import pygame
from src.Misc import Misc
from src.Globals import settings


class UI:
    def __init__(self, size: tuple[float, float], bold=True):
        width, height = size

        self.border_size = height * 0.05
        self.bold = bold
        self.width = width
        self.height = height

        self.font_size = int(height * 0.6)
        self.font = self.get_font()

        self.bg_color: tuple[int, int, int] = settings.Color.DARK_GREY
        self.font_color:  tuple[int, int, int] = settings.Color.OFF_WHITE
        self.border_color: tuple[int, int, int] = settings.Color.BLACK

        self.rect = pygame.Rect(0, 0, width, height)

    def get_font(self, is_italic=True):
        return Misc.get_font(settings.Font_Names.HUD, self.font_size, self.bold, is_italic)
