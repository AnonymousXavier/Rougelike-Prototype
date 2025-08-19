import pygame
from src.Misc.Sprite import Sprite


class Item(Sprite):
    def __init__(self, sheet: pygame.Surface, frames: list[pygame.Rect], item_stat_info):
        super().__init__(sheet, frames)

        self.name = item_stat_info.name
        self.description = item_stat_info.description

