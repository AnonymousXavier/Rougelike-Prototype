import pygame
from src.Core.Items.Consumable import Consumable
from src.Core.Entities.Player import Player
from src.Globals import Cache, settings
from src.Misc import Misc
from src.UI.panel import Panel
from src.UI.label import Label
from src.UI.progress_bar import Progress_Bar


class Player_HUD_Display():
    def __init__(self, player: Player) -> None:
        self.player: Player = player
        self.health_bar = Progress_Bar(self.player.xp_goal, ((settings.PLAYER_XP_BAR_WIDTH - settings.SCREEN_MARGIN, settings.PLAYER_XP_BAR_HEIGHT)))
        self.xp_bar = Progress_Bar(self.player.xp_goal, ((settings.PLAYER_XP_BAR_WIDTH - settings.SCREEN_MARGIN, settings.PLAYER_XP_BAR_HEIGHT)))
        self.faceset = Cache.Sprites.Facesets.Green_Ninja
        self.name_and_score_label = Label("", (settings.PLAYER_NAME_AND_LEVEL_LABEL_WIDTH, settings.PLAYER_NAME_AND_LEVEL_LABEL_HEIGHT))
        self.hud_panel = Panel((10, 10))
        self.faceset_rect = pygame.Rect()
        self.name_and_label_text_width = 19

        self.init()

    def draw(self, surface: pygame.Surface):
        self.hud_panel.draw(surface)
        self.health_bar.draw(surface)
        self.xp_bar.draw(surface)
        self.name_and_score_label.draw(surface)

        surface.blit(self.faceset, self.faceset_rect)

    def update(self, dt: float):
        self.name_and_score_label.text = Misc.fill_text(self.name_and_label_text_width, self.player.name, f"Lvl {self.player.level}")
        self.health_bar.value = self.player.health
        self.health_bar.maxValue = self.player.max_health
        self.xp_bar.value = self.player.xp
        self.xp_bar.maxValue = self.player.xp_goal

        self.name_and_score_label.update()
        self.health_bar.update(dt)
        self.xp_bar.update(dt)

    def init(self):
        # Faceset
        self.faceset_rect = self.faceset.get_rect(topleft=(settings.SCREEN_MARGIN, settings.SCREEN_MARGIN))

        # Player Name and Score Label
        self.name_and_score_label.text = Misc.fill_text(self.name_and_label_text_width, self.player.name, f"Lvl {self.player.level}")
        self.name_and_score_label.update()
        self.name_and_score_label.rect.left = self.faceset_rect.right + settings.SCREEN_MARGIN
        self.name_and_score_label.rect.top = self.faceset_rect.top

        # Health Bar
        self.health_bar.bg_color = settings.Color.DARKER_GREY
        self.health_bar.rect.left = settings.SCREEN_MARGIN + self.faceset_rect.right
        self.health_bar.rect.top = settings.SCREEN_MARGIN + self.name_and_score_label.rect.bottom

        # XP Bar
        self.xp_bar.font_color = settings.Color.GREY
        self.xp_bar.bar_color = settings.Color.LIGHT_YELLOW
        self.xp_bar.bg_color = settings.Color.DARKER_GREY
        self.xp_bar.rect.left = self.health_bar.rect.left
        self.xp_bar.rect.top = self.health_bar.rect.bottom + settings.SCREEN_MARGIN

        # BG Panel
        self.hud_panel.rect.width = self.health_bar.rect.right - self.faceset_rect.left + settings.SCREEN_MARGIN * 2
        self.hud_panel.rect.height = self.xp_bar.rect.bottom - self.name_and_score_label.rect.top + settings.SCREEN_MARGIN * 2
        self.hud_panel.rect.topleft = self.faceset_rect.topleft