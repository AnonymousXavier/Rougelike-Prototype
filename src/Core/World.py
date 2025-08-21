import pygame
import random

import src.Globals.settings as settings
from src.Globals import Enums
from src.Globals.Cache import Sprites

from src.Core.Entities.Entities import Entities
from src.Core.Entities.Player import Player
from src.Core.Entities.Enemy import Enemy

from src.Core.World_Generation.world_generator import World_Generator

from src.Core.Interactables.Interactables import Interactable
from src.Core.Interactables.Chest import Chest
from src.Core.Interactables.Bush import Bush

from src.Misc.Camera import Camera
from src.Misc import Misc

class World_Enemies_Data:
    def __init__(self) -> None:
        self.alive = 0
        self.total = 0
    
class World:
    def __init__(self, n=None):
        self.window = pygame.display.get_surface()
        self.hud = None
        self.current_room_count = n or settings.INITIAL_ROOM_COUNT
        self.floor = self.current_room_count - settings.INITIAL_ROOM_COUNT

        self.world_generator = World_Generator(min(settings.MAX_GENERATABLE_ROOMS_COUNT, self.current_room_count))
        self.entities_map: list[list[None | Entities]] = []
        self.items_map: list[list[Interactable]] = []
        self.enemies_data = World_Enemies_Data()

        self.player = Player(0)
        self.camera = Camera()      
        self.finished_initializing = False
        self.ready_to_move_to_next_floor = False

        self.is_a_movement_key_pressed = False
        self.last_key_pressed = 0
        self.frames_holding_key = 0
        self.game_update_delay = 15 # Delay in case ur holding the key for long

    def get_player_start_position(self):
        room = self.world_generator.rooms[0]
        w = h = room.size
        x, y = room.top_left

        return x + int(w / 2), y + int(h / 2)

    def get_room_index_of(self, pos: tuple[int, int]):
        for i, room in enumerate(self.world_generator.rooms):
            if room.is_inside(pos):
                return i
        return -1 # Could be at the door!
                
    def create_items_map(self):
        grid_map = self.world_generator.grid
        items_map: list[list[Interactable | None]] = [[None for _ in range(len(grid_map[0]))] for __ in range(len(grid_map))]
        
        chest_spawn_chance = settings.CHEST_SPAWN_CHANCE
        bush_unspawn_chance = settings.BUSH_SPAWN_CHANCE

        for room in self.world_generator.rooms:
            l, t = room.top_left # Top Left  # noqa: E741
            r, b = l + room.size - 1, t + room.size - 1 # Bottom Right

            options = [(l, t), (r, t), (l, b), (r, b)] # 4 Corners of room
            choice = random.choice(options)
            x, y = choice

            # Spawn Bushes
            for by in range(t, b + 1):
                for bx in range(l, r + 1):
                    if by - t in (0, room.size - 1) or bx - l in (0, room.size - 1):
                        if random.randint(0, bush_unspawn_chance) != bush_unspawn_chance: 
                            continue
                        if self.entities_map[by][bx] or self.world_generator.grid[by][bx] != Enums.World_Types.FLOOR: 
                            continue
                        
                        bush = Bush()
                        bush.pos = (bx, by)
                        items_map[by][bx] = bush

            # Spawn Treasure
            if random.randint(0, chest_spawn_chance) == chest_spawn_chance:
                while grid_map[y][x] != Enums.World_Types.FLOOR or self.will_block_room_passage((x, y)):
                    if len(options) == 0: 
                        break
                    options.remove(choice)

                    choice = random.choice(options)
                    x, y = choice

                if len(options) > 0: 
                    chest = Chest()
                    chest.pos = x, y
                    items_map[y][x] = chest

        return items_map

    def will_block_room_passage(self, pos:tuple[int, int]):
        blocks_around_coord = self.get_entities_around(pos, self.world_generator.grid)
        for block in blocks_around_coord:
            if block == Enums.World_Types.DOOR: 
                return True
        return False

    def create_entities_map(self):
        entities_map = []
        grid_map = self.world_generator.grid

        cx, cy = self.get_player_start_position()

        for i in range(len(grid_map)):
            row = []

            for j in range(len(grid_map[0])):
                cell = grid_map[i][j]

                if cell == Enums.World_Types.FLOOR: 
                    n = random.randint(0, settings.ENEMY_SPAWN_CHANCE)
                    if n == settings.ENEMY_SPAWN_CHANCE:
                        floor = self.floor
                        enemy = Enemy(Enums.ENEMIES.CYCLOPS)
                        if floor > 0:
                            enemy.level = random.randint(max(1, int(floor / 2)), floor + 1)
                            enemy.update_stats()
                        enemy.pos = (j, i)
                        self.enemies_data.total += 1
                        enemy.room_id = self.get_room_index_of(enemy.pos)
                        row.append(enemy)

                row.append(None)
            entities_map.append(row)

        # Add Player to Map
        self.player.pos = cx, cy
        entities_map[cy][cx] = self.player

        return entities_map

    def draw(self):
        is_done_generating = self.world_generator.is_done_generating
        if is_done_generating:
            self.draw_map()

    def get_grid_size(self):
        return Misc.get_grid_size(self.world_generator.grid)

    def get_camera_rect(self):
        grid_width, grid_height = self.get_grid_size()
        return self.camera.get_rect(grid_width, grid_height)

    def draw_map(self):
        grid_map = self.world_generator.grid
        w = h = settings.ROOM_CELL_WIDTH
        
        camera_rect = self.get_camera_rect()
        draw_area = pygame.Surface(camera_rect.size)

        for grid_y in range(camera_rect.top, camera_rect.bottom):
            i = grid_y - camera_rect.top
            for grid_x in range(camera_rect.left, camera_rect.right):
                j = grid_x - camera_rect.left
                cell = grid_map[grid_y][grid_x]

                y, x = i * h, j * w
                rect = pygame.Rect(x, y, w, h)

                sprite = pygame.Surface((0, 0))
                # Layer 1: Map
                match cell:
                    case Enums.World_Types.WALL:
                        sprite = Sprites.Tiles.wall
                    case Enums.World_Types.FLOOR:
                        sprite = Sprites.Tiles.floor
                    case Enums.World_Types.DOOR:
                        sprite = Sprites.Tiles.pathway
                    case Enums.World_Types.BLANKS:
                        sprite = Sprites.Tiles.blank
                    case Enums.World_Types.STAIR:
                        sprite = Sprites.Tiles.stair
                
                draw_area.blit(sprite, rect)

                # Layer 2: interactables
                if self.items_map:
                    item = self.items_map[grid_y][grid_x]
                    if item:
                        item.rect = rect
                        draw_area.blit(item.get_image(), rect)

                # Layer 3: Entities
                if self.entities_map:
                    entity = self.entities_map[grid_y][grid_x]
                    if entity:
                        entity.rect = rect
                        draw_area.blit(entity.get_image(), rect)
                        
        camera_render = pygame.transform.scale_by(draw_area, settings.ZOOM)
        self.window.blit(camera_render)

    def get_entities_around(self, ref_pos: tuple[int, int], temp_map: list[list], distance = 1):
        enemies_in_range: list = []
        grid_width, grid_height = Misc.get_grid_size(temp_map)

        rx, ry = ref_pos
        tx, ty = max(0, rx - distance), max(0, ry - distance) # Top Left coords
        bx, by = min(rx + distance, grid_width), min(ry + distance, grid_height) # Bottom Right Coors

        for i in range(ty, by + 1):
            for j in range(tx, bx + 1):
                if i == ry and j == rx: 
                    continue
                cell = temp_map[i][j]
                if cell is not None: 
                    enemies_in_range.append(cell)

        return enemies_in_range

    def process_attacks(self, temp_map: list[list]):
        dead_enemies_pos = []
        enemies_in_range: list[Entities] = self.get_entities_around(self.player.pos, temp_map)

        # Enemies Attack Player and vice versa
        player_attack_target = self.player.get_next_path_pos()
        
        for enemy in enemies_in_range:
            enemy_attack_target = enemy.get_next_path_pos()

            if player_attack_target == enemy.pos:
                enemy.hurt_by(self.player.get_damage())

            if not enemy.is_dead():
                if enemy_attack_target == self.player.pos: 
                    self.player.hurt_by(enemy.damage)
            else: 
                dead_enemies_pos.append((enemy.pos))

        # Remove dead enemies
        for (x, y) in dead_enemies_pos:
            self.player.earn_xp_from(temp_map[y][x])
            temp_map[y][x] = None

    def count_enemies_in_room(self, room_index: int):
        room = self.world_generator.rooms[room_index]
        entities_count = 0
        tx, ty = room.top_left
        w = h = room.size

        for i in range(ty, ty + h + 1):
            for j in range(tx, tx + w + 1):
                cell = self.entities_map[i][j]
                if cell and cell != self.player: 
                    print("Entity Found At: ", j, i, cell)
                    entities_count += 1

        return entities_count
    
    def update_map(self):
        # Update Entities
        temp_map: list[list[Entities | None]] = Misc.clone_2D_array(self.entities_map)
        px, py = self.player.pos
        
        # Move Player
        if not self.player.interact_with_interactables(self.items_map): # If player didnt interact with anything
            x, y = self.player.move(self.get_collisions_grid(temp_map))
            temp_map[py][px] = None
            temp_map[y][x] = self.player

        # Move Everyone eLse
        self.enemies_data.alive = 0
        for grid_y, row in enumerate(self.entities_map):
            for grid_x, entity in enumerate(row):
                if entity:
                    # Handle PathFinding
                    if entity is not self.player:
                        self.enemies_data.alive += 1
                        entity.target = None
                        if (entity.room_id == self.player.room_id and entity.can_see(self.player.pos)) or entity.can_see(self.player.pos):
                            entity.target = self.player.pos

                        # Move Entity
                        collision_grid = self.get_collisions_grid(temp_map)
                        entity.update(collision_grid) # Calculate Move Direction and Update it
                        x, y = entity.move(collision_grid)

                        temp_map[grid_y][grid_x] = None
                        temp_map[y][x] = entity

        # Make Everyone attack
        self.process_attacks(temp_map)

        px, py = self.player.pos
        # Check if player is over a stair:
        stair_x, stair_y = self.world_generator.stair_coords[1]
        if px == stair_x and py == stair_y: 
            self.ready_to_move_to_next_floor = True

        self.entities_map = temp_map
        self.entities_map[py][px] = self.player

    def get_collisions_grid(self, entities_map_clone=None):
        collision_grid = Misc.clone_2D_array(entities_map_clone if entities_map_clone else self.entities_map)
        for i, row in enumerate(self.world_generator.grid):
            for j, cell in enumerate(row):
                if cell == Enums.World_Types.WALL: 
                    collision_grid[i][j] = cell
                elif self.items_map[i][j] and not self.items_map[i][j].can_walk_over: 
                    collision_grid[i][j] = self.items_map[i][j]
        return collision_grid

    def get_screen_sector_center(self):
        # Divide the Screen into sectors, each about the size of the camera's view
        # Move the Camera to this center each time the player gets outta bounds

        sector_scale = 2.25 # Scale of sector to camera's view
        camera_rect = self.get_camera_rect()
        w, h = camera_rect.right - camera_rect.left, camera_rect.bottom - camera_rect.top
        sw, sh = w / sector_scale, h / sector_scale
        
        px, py = self.player.pos
        sx, sy = round(px / sw), round(py / sh) # Sector Coordinates of Player

        tx, ty = sx * sw , sy * sh # Top left position
        cx, cy = tx + sw / 2, ty + sh / 2

        return cx, cy 

    def get_attackable_enemies(self):
        attackable_enemies = self.get_entities_around(self.player.pos, self.entities_map)
        return [enemy for enemy in attackable_enemies if enemy.get_next_path_pos() == self.player.pos]

    def update_camera(self, dt: float):
        self.camera.target = self.get_screen_sector_center()
        self.camera.update(dt)

    def update(self, dt: float):
        if not self.world_generator.is_done_generating: 
            self.world_generator.update(dt)
        else:
            if not self.entities_map: 
                self.entities_map = self.create_entities_map()
                self.items_map = self.create_items_map()
                self.finished_initializing = True
            if self.is_a_movement_key_pressed: 
                self.update_game()

            self.update_camera(dt)

    def update_current_room(self):
        self.player.room_id = self.get_room_index_of(self.player.pos)

    def update_game(self):
        if self.hud.inventory_display_hud.visible:
            return
        if self.frames_holding_key % self.game_update_delay == 0:
            self.player.process_input(self.last_key_pressed)
            self.update_current_room()
            self.update_map()
        
        self.frames_holding_key += 1

    def process_input(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            self.is_a_movement_key_pressed = event.key in settings.Controls.MOVEMENT
            self.last_key_pressed = event.key
        elif event.type == pygame.KEYUP:
            self.is_a_movement_key_pressed = False
            self.frames_holding_key = 0

                    