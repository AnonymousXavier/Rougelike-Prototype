import pygame
from src.Misc import Misc
from src.Globals import settings, Cache, Enums
from src.Misc.Spritesheet import SpriteSheet
from src.Globals.Cache import Sprites, Stats_Info
from src.Core.Entities.Entities import Entities
from src.Core.Interactables.Interactables import Interactable
from src.Misc.Inventory import Inventory


class Buffs:
    health = 0
    damage = 0

class Player(Entities):
    def __init__(self, id: int):
        spriteSheet: SpriteSheet = Sprites.Heroes.ALL[id]
        stats = Stats_Info.Heroes[id]
        super().__init__(spriteSheet.image, spriteSheet.get_frames()[0], stats)

        self.name = "Green Ninja"

        self.skill_points = 0
        self.max_health = self.health
        self.bonus_health = 0
        self.bonus_damage = 0

        self.xp = 0
        self.xp_goal = 8
        self.inventory = Inventory()
        self.kills = 0

        self.general_upgrade_factor = 1.1
        self.xp_upgrade_factor = 1.75

        self.passive_buffs: list[Cache.Consumable_Buff] = []
        self.buff = Buffs() # A cumulative way of storing buff values

    def earn_xp_from(self, entity: Entities):
        self.xp += Misc.calculate_xp_gain_from_kill(entity, self)
        self.level_up_if_can()
        self.kills += 1
        Cache.Audio.Sound.XP.play()
        
    def level_up_if_can(self):
        diff = self.xp_goal - self.xp
        if diff <= 0:
            self.level_up()

    def level_up(self):
        self.xp = abs(self.xp_goal - self.xp)
        self.level += 1
        self.skill_points += settings.PLAYER_SKILL_POINTS_PER_UPGRADE
        self.xp_goal *= self.xp_upgrade_factor
        self.max_health *= self.general_upgrade_factor
        self.health = self.get_max_health()
        self.damage *= self.general_upgrade_factor
        Cache.Audio.Sound.LEVEL_UP.play()

    def interact_with_interactables(self, interactables_map: list[list]):
        px, py = self.pos
        dx, dy = self.direction
        x, y =  Misc.clamp(px + dx, 0, len(interactables_map[0]) - 1), Misc.clamp(py + dy, 0, len(interactables_map) - 1)

        interactable_obj = interactables_map[y][x]
        if isinstance(interactable_obj, Interactable) and not interactable_obj.can_walk_over:
            interactable_obj.interact(self)
            self.xp += interactable_obj.xp_worth # Earn XP from Interaactables
            self.level_up_if_can()
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

    def get_max_health(self):
        return (self.max_health * (1 + self.bonus_health)) * (1 + self.buff.health)

    def get_damage(self):
        return (self.damage * (1 + self.bonus_damage)) * (1 + self.buff.damage)

    def increase_health_buff(self):
        self.bonus_health += settings.PLAYER_BUFF_INCREASE_PERCENT
        self.skill_points -= 1

    def increase_damage_buff(self):
        self.bonus_damage += settings.PLAYER_BUFF_INCREASE_PERCENT
        self.skill_points -= 1

    def update(self, grid_map: list[list[int, int]]):
        super().update(grid_map)
        self.update_buffs()

    def update_buffs(self):
        expired_buffs = []
        self.buff.health = 0
        self.buff.damage = 0

        for passive_buff in self.passive_buffs:

            passive_buff.update()
            if passive_buff.duration <= 0:
                expired_buffs.append(passive_buff)
            else:
                self.apply_buff(passive_buff)

        for buff in expired_buffs:
            self.passive_buffs.remove(buff)

    def apply_buff(self, buff: Cache.Consumable_Buff):
        match buff.id:
            case Enums.CONSUMABLES.CALAMARI:
                self.buff.damage += 1 # 100% bonus
            case Enums.CONSUMABLES.BEEF:
                self.buff.health += 1 # 100% bonus
