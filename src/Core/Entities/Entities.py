import random
import pygame
from src.Misc.Sprite import Sprite
from src.Misc import Misc
from src.Globals import Enums


class Entities(Sprite):
    def __init__(self, sheet: pygame.Surface, frames: list[pygame.Rect], stats_info):
        super().__init__(sheet, frames)

        self.name = stats_info.name
        self.room_id = 0
        self.target: tuple[int, int] | None = None

        self.max_health = stats_info.health
        self.health = self.max_health
        self.damage = stats_info.damage
        self.level = 1

        self.sight_range = 5
        self.direction = (0, 0)

    def update_stats(self):
        self.max_health = self.max_health * self.level
        self.damage = self.damage * self.level
        self.health = self.max_health

    def update_direction(self, grid_map: list[list]):
        if self.target is None: 
            self.direction = random.choice(Enums.DIRECTIONS.ALL)
        else:
            self.direction = self.move_towards(grid_map, self.target)
        self.update_sprite()

    def can_see(self, target: tuple[int, int]):
        return self.is_next_to(target, self.sight_range)
    
    def is_next_to(self, target: tuple[int, int], max_distance=1):
        tx, ty = target
        px, py = self.pos

        dx, dy = tx - px, ty - py
        magnitude = Misc.get_vector_magnitude((dx, dy))

        return magnitude <= max_distance
    
    def get_next_path_pos(self):
        x, y = self.pos
        dx, dy = self.direction
        return x + dx, y + dy

    def move_towards(self, grid_map: list[list], target: tuple[int, int]):
        tx, ty = target
        px, py = self.pos

        hor_option = Enums.DIRECTIONS.LEFT if tx < px else Enums.DIRECTIONS.RIGHT
        ver_option = Enums.DIRECTIONS.UP if ty < py else Enums.DIRECTIONS.DOWN

        hx_off, hy_off = hor_option
        vx_off, vy_off = ver_option
        h_pos = (px + hx_off, py + hy_off)
        v_pos = (px + vx_off, py + vy_off)

        if h_pos == target: 
            return hor_option
        if v_pos == target: 
            return ver_option

        # Check blocked status
        h_blocked = grid_map[h_pos[1]][h_pos[0]] is not None
        v_blocked = grid_map[v_pos[1]][v_pos[0]] is not  None

        # Distance to target from each move
        h_dist = abs(h_pos[0] - tx) + abs(h_pos[1] - ty)
        v_dist = abs(v_pos[0] - tx) + abs(v_pos[1] - ty)

        # If neither r blocked, pick the one closer to target
        if not v_blocked and not h_blocked:
            return hor_option if h_dist < v_dist else ver_option

        # If vertical path is blocked, go horizontal and vice versa
        if v_blocked and not h_blocked: 
            return hor_option
        if h_blocked and not v_blocked: 
            return ver_option
        return (0, 0)

    def move(self, map_collision_grid: list[list[int]]):
        px, py = self.pos
        dx, dy = self.direction

        x, y =  Misc.clamp(px + dx, 0, len(map_collision_grid[0]) - 1), Misc.clamp(py + dy, 0, len(map_collision_grid) - 1)
        x, y = int(x), int(y)

        if map_collision_grid[y][x] is None: 
            self.pos = (x, y)
            return x, y
        
        return px, py

    def update_sprite(self):
        match self.direction:
            case Enums.DIRECTIONS.LEFT:
                self.state = Enums.SPRITE_INDEX.LEFT
            case Enums.DIRECTIONS.RIGHT:
                self.state = Enums.SPRITE_INDEX.RIGHT
            case Enums.DIRECTIONS.UP:
                self.state = Enums.SPRITE_INDEX.UP
            case Enums.DIRECTIONS.DOWN:
                self.state = Enums.SPRITE_INDEX.DOWN

    def is_dead(self):
        return self.health <= 0

    def hurt_by(self, dmg: float):
        self.health -= dmg
        return self.is_dead()

    def update(self, grid_map: list[list[int, int]]):
        pass