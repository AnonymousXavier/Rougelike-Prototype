import pygame
from src.Misc import Misc
from src.Globals import settings
from src.Misc.Spritesheet import SpriteSheet
from src.Globals.Cache import Sprites, Stats_Info
from src.Core.Entities.Entities import Entities
from src.Core.Interactables.Interactables import Interactable
from src.Misc.Inventory import Inventory

class Player(Entities):
    def __init__(self, id: int):
        spriteSheet: SpriteSheet = Sprites.Heroes.ALL[id]
        stats = Stats_Info.Heroes[id]
        super().__init__(spriteSheet.image, spriteSheet.get_frames()[0], stats)

        self.name = "Green Ninja"
        self.health = 25
        self.max_health = self.health
        self.xp = 0
        self.xp_goal = 32
        self.inventory = Inventory()

        self.general_upgrade_factor = 1.1
        self.xp_upgrade_factor = 2

    def earn_xp_from(self, entity: Entities):
        self.xp += Misc.calculate_xp_gain_from_kill(entity, self)
        diff = self.xp_goal - self.xp
        if diff <= 0:
            self.level_up()

    def level_up(self):
        self.xp = abs(self.xp_goal - self.xp)
        self.level += 1
        self.xp_goal *= self.xp_upgrade_factor
        self.max_health *= self.general_upgrade_factor
        self.health = self.max_health
        self.damage *= self.general_upgrade_factor

    def interact_with_interactables(self, interactables_map: list[list]):
        px, py = self.pos
        dx, dy = self.direction
        x, y =  Misc.clamp(px + dx, 0, len(interactables_map[0]) - 1), Misc.clamp(py + dy, 0, len(interactables_map) - 1)

        interactable_obj = interactables_map[y][x]
        if isinstance(interactable_obj, Interactable) and not interactable_obj.can_walk_over:
            interactable_obj.interact(self)
            return True
        return False

    def process_input(self, key: int):
        controls = settings.Controls
        dx, dy = 0, 0

        if key in controls.LEFT:
            dx = -1
        elif key in controls.RIGHT:
            dx = 1
        elif key in controls.UP:
            dy = -1
        elif key in controls.DOWN:
            dy = 1

        self.direction = dx, dy
        self.update_sprite()
