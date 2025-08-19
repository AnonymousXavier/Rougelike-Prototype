import pygame
from src.Misc.UI import UI


class Label(UI):
    def __init__(self, text: str, size: tuple[float, float], bold=True):
        width, _ = size
        self.size = size
        self.font_size = width * 0.7
        super().__init__(size, bold=bold)

        self.text = text
        self.text_surface: pygame.Surface = pygame.Surface((10, 10))
        self.capitalize = True
        self.centered = False

    def update_text_surface(self):
        self.text_surface = self.font.render(self.text if not self.capitalize else self.text.upper(), True, self.font_color)
        self.rect = self.text_surface.get_rect(topleft=self.rect.topleft)

    def update(self):
        self.update_text_surface()

    def get_centered_text(self):
        temp_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        temp_surface.blit(self.text_surface, self.text_surface.get_rect(center=temp_surface.get_rect().center))
        return temp_surface 

    def draw(self, surface: pygame.Surface):
        text_surface = self.text_surface
        if self.centered:
              text_surface = self.get_centered_text()
        surface.blit(text_surface, self.rect)