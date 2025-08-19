import pygame
from src.Misc import Misc


class Sprite:
    def __init__(self, sheet: pygame.Surface, frames: list[pygame.Rect]):
        self.name = ""
        self.id = 0

        self.sheet = sheet
        self.frames = frames
        self.state = 0
        self.rect = pygame.Rect()
        self.pos: tuple[int, int] = (0, 0)

        self.flip_h = False
        self.flip_v = False
        self.rotated_angle = 0

    def get_image(self):
        sprite = Misc.create_sprite((self.rect.width, self.rect.height), self.sheet, self.frames[self.state])
        sprite = pygame.transform.flip(sprite, self.flip_h, self.flip_v)
        return Misc.rotate_surface(sprite, self.rotated_angle)