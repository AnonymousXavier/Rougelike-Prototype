import pygame
from src.Globals import settings
from src.Misc.UI import UI


class Panel(UI):
    def __init__(self, size: tuple[float, float]):
        super().__init__(size)
        self.border_size = size[1] * 0.02 * settings.ZOOM
        self.border_radius = 5
        self.has_border = False

    def draw(self, surface: pygame.Surface):
        if self.has_border:
            border_rect = pygame.Rect(0, 0, self.rect.width + self.border_size * 2, self.rect.height + self.border_size * 2)
            border_rect.center = self.rect.center

            pygame.draw.rect(surface, self.border_color, border_rect, 0, self.border_radius)
        pygame.draw.rect(surface, self.bg_color, self.rect, 0, self.border_radius)