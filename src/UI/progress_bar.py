import pygame
from src.Misc import Misc
from src.Misc.UI import UI
from src.Globals import settings

pygame.init()

class Progress_Bar(UI):
    def __init__(self, maxValue: float, size: tuple[float, float]):
        super().__init__(size)

        self.bar_color: tuple[int, int, int] = settings.Color.RED

        self.bar_size = (0, 0)
        self.full_size = size
        self.speed_scale = 0.1

        self.value: float = maxValue
        self.maxValue: float = maxValue

        self.show_text = True

    def get_bar_surface(self):
        bar_surface = pygame.Surface((self.width, self.height))

        full_width, full_height = self.full_size
        bar_width, bar_height = self.bar_size     

        bg_bar = pygame.Rect(self.border_size, self.border_size, full_width, full_height)
        progress_bar = pygame.Rect(self.border_size, self.border_size, bar_width, bar_height)
        
        pygame.draw.rect(bar_surface, self.bg_color, bg_bar)
        pygame.draw.rect(bar_surface, self.bar_color, progress_bar)

        return bar_surface

    def draw_text(self, bar_surface: pygame.Surface):
        text = f"{round(self.value)} / {round(self.maxValue)}"
        
        text_surface = self.font.render(text, True, self.font_color)
        text_rect = text_surface.get_rect(center = bar_surface.get_rect().center)
        bar_surface.blit(text_surface, text_rect)

    def draw(self, surface: pygame.Surface):
        bar_surface = self.get_bar_surface()
        if self.show_text: 
            self.draw_text(bar_surface)

        surface.blit(bar_surface, self.rect)

    def update(self, dt: float):
        self.full_size = self.width - self.border_size * 2, self.height - self.border_size * 2
        factor = self.value / self.maxValue

        full_width, full_height = self.full_size
        prev_bar_width = self.bar_size[0]

        goal_bar_width = factor * full_width

        width_diff = goal_bar_width - prev_bar_width

        transition_increment = max(0.3, abs(width_diff) * dt * self.speed_scale) * Misc.sign(width_diff)

        self.bar_size = prev_bar_width + transition_increment, full_height



