import pygame
from src.Globals import settings


class Cell:
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c
        self.x = 0
        self.y = 0
        self.cx = 0
        self.cy = 0

        self.is_taken = False
        self.options = [
            (-1, 0), # Left
            (1, 0), # Right
            (0, -1), # Up
            (0, 1), # Down
        ]
        
        self.init()

    def init(self):
        dx, dy = settings.SCREEN_WIDTH - settings.GRID_WIDTH, settings.SCREEN_HEIGHT - settings.GRID_HEIGHT
        ox, oy = dx / 4, dy / 4

        self.x = self.r * (settings.CELL_WIDTH + settings.CELL_SPACING) + ox
        self.y = self.c * (settings.CELL_HEIGHT + settings.CELL_SPACING) + oy

        self.cx, self.cy = self.x + settings.MARKER_RADIUS, self.y + settings.MARKER_RADIUS

    
    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, settings.VISITED_MARKER_COLOR, (self.cx, self.cy), settings.MARKER_RADIUS)

    def get_option_index(self, option_to_index: tuple[int, int]):
        ox1, oy1 = option_to_index
        for i, option in enumerate(self.options):
            ox2, oy2 = option
            if ox1 == ox2 and oy1 == oy2: return i
        return - 1