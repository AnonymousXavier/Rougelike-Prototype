import pygame
from src.Misc.Sprite import Sprite
from src.Globals import Enums


class Interactable(Sprite):
    def __init__(self, sheet: pygame.Surface, frames: list[pygame.Rect]):
        super().__init__(sheet, frames)
        self.rarity = Enums.RARITY.COMMON
        self.can_walk_over = False
        self.content = []
        self.xp_worth = 0

    def interact(self, player):
        self.state = Enums.INTERACTABLES_STATES.OPEN
        for item in self.content:
            player.inventory.add(item)
