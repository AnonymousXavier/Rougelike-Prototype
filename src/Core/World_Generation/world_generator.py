import random
import pygame
import time
from src.Misc.Room import Room
from src.Globals.Enums import World_Types
from src.Globals import settings
from src.Core.World_Generation.drunkards_walk import Drunkards_Walk

class World_Generator:
    def __init__(self, rooms):
        self.number_of_rooms = self.get_optimal_room_count(rooms)
        print("Generated: ", self.number_of_rooms, " Rooms")
        self.seed = int(time.time())
        random.seed(self.seed)
        self.drunkards_walk = Drunkards_Walk(rooms)
        self.grid: list[list[int]] = []
        self.start_step_point = (0, 0)

        self.margin = settings.ROOM_PADDING
        self.is_done_generating = False
        self.player_spawn_position = (0, 0)
        self.rooms: list[Room] = []
        self.stair_coords = []

    def get_optimal_room_count(self, room_count):
        if room_count > settings.GRID_COLS * 2:
            return settings.GRID_COLS * 2
        return room_count

    def create_grid(self):
        grid = []

        max_rows = max_cols = 0
        min_rows = min_cols = float("inf")

        for cell in self.drunkards_walk.taken_cells:
            if cell.r > max_rows:
                max_rows = cell.r
            if cell.c > max_cols:
                max_cols = cell.c
            if cell.r < min_rows:
                min_rows = cell.r
            if cell.c < min_cols:
                min_cols = cell.c

        min_rows, min_cols = int(min_rows), int(min_cols)
        mx, my = self.margin
 
        map_rows = (max_rows - min_rows + 1 + mx) * settings.DEFAULT_ROOM_SIZE
        map_cols = (max_cols - min_cols + 1 + my) * settings.DEFAULT_ROOM_SIZE
       
        for _ in range(map_rows):
            row = []
            for _ in range(map_cols):
                row.append(World_Types.BLANKS)
            grid.append(row)
        
        self.start_step_point = (min_cols, min_rows)
        return grid

    def draw(self, surface: pygame.Surface):
        if not self.grid:
            self.drunkards_walk.draw(surface)
        else:
            self.draw_grid(surface)

    def draw_grid(self, surface: pygame.Surface):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):

                x = i * (settings.ROOM_CELL_WIDTH + settings.ROOM_CELL_SPACING)
                y = j * (settings.ROOM_CELL_HEIGHT + settings.ROOM_CELL_SPACING)

                color = settings.ROOM_COLOR
                if value == World_Types.DOOR: 
                    color = settings.DOOR_COLOR
                if value == World_Types.BLANKS: 
                    color = settings.BLANKS_COLOR
                if value == World_Types.WALL: 
                    color = settings.WALL_COLOR

                rect = pygame.Rect(x, y, settings.ROOM_CELL_WIDTH, settings.ROOM_CELL_HEIGHT)
                pygame.draw.rect(surface, color, rect)

    def upgrade_grid_with_stair(self):
        start_room, end_room = self.rooms[0], self.rooms[len(self.rooms) - 1]
        
        x1, y1 = start_room.top_left
        x2, y2 = end_room.top_left

        stair1_x, stair1_y = x1 + random.randint(1, start_room.size - 1), y1 + random.randint(1, start_room.size- 1)
        stair2_x, stair2_y = x2 + random.randint(1, end_room.size - 1), y2 + random.randint(1, end_room.size - 1)

        self.grid[stair1_y][stair1_x] = World_Types.STAIR
        self.grid[stair2_y][stair2_x] = World_Types.STAIR

        self.stair_coords = [(stair1_x, stair1_y), (stair2_x, stair2_y)]

    def translate_step_to_grid_pos(self, cell, direction, index):
        offset = int(settings.DEFAULT_ROOM_SIZE / 2)
        dx, dy = direction
        mx, my = self.margin
        sx, sy = self.start_step_point

        r = (cell.r - sy) * settings.DEFAULT_ROOM_SIZE + dy * index + offset + mx
        c = (cell.c - sx) * settings.DEFAULT_ROOM_SIZE + dx * index + offset + my

        return c, r

    def update_grid_with_new_path(self):
        mx, my = self.margin
        prev_cell = self.drunkards_walk.taken_cells[0]
        offset = int(settings.DEFAULT_ROOM_SIZE / 2)
        sx, sy = self.start_step_point

        for step_index, cell in enumerate(self.drunkards_walk.taken_cells):
            dx, dy = cell.c - prev_cell.c, cell.r - prev_cell.r
            # Draw a straight line all the way to the next
            for i in range(settings.DEFAULT_ROOM_SIZE):
                c, r = self.translate_step_to_grid_pos(prev_cell, (dx, dy), i)

                if step_index == 0:
                    if i == offset:
                        self.player_spawn_position = c, r

                self.grid[r][c] = World_Types.DOOR
            prev_cell = cell

    def update_grid_with_rooms(self):
        mx, my = self.margin
        for cell in self.drunkards_walk.taken_cells:
            removed_room_size = random.randint(1, round(settings.DEFAULT_ROOM_SIZE / 2) - 1)

            sx, sy = self.start_step_point
            r = (cell.r - sy)  * settings.DEFAULT_ROOM_SIZE - removed_room_size + mx
            c = (cell.c - sx) * settings.DEFAULT_ROOM_SIZE - removed_room_size + my

            room = Room(c + removed_room_size, r + removed_room_size, settings.DEFAULT_ROOM_SIZE - removed_room_size)
            self.rooms.append(room)

            for i in range(settings.DEFAULT_ROOM_SIZE - removed_room_size):
                for j in range(settings.DEFAULT_ROOM_SIZE - removed_room_size):
                    self.grid[r + i + removed_room_size][c + j + removed_room_size] = World_Types.FLOOR

    def update_grid_with_walls(self):
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == World_Types.BLANKS:
                    found_non_blank = False
                    # Check Adjacent Cells for a non Blank
                    for dy in range(-1, 2, 1):
                        if found_non_blank: 
                            break
                        for dx in range(-1, 2, 1):
                            r, c = max(0, dy + i), max(0, dx + j)
                            r, c = min(r, len(self.grid) - 1), min(c, len(self.grid[0]) - 1)

                            if self.grid[r][c] in (World_Types.DOOR, World_Types.FLOOR):
                                found_non_blank = True
                                break
                    if found_non_blank: 
                        self.grid[i][j] = World_Types.WALL
                            
    def update(self, dt: float):
        is_done_generating_path = self.drunkards_walk.has_reached_max_steps() or self.drunkards_walk.has_filled_grid()
        
        if not is_done_generating_path: 
            self.drunkards_walk.update(dt)
        
        elif not self.grid:
            self.grid = self.create_grid()
            self.update_grid_with_drunken_walks_path()

    def update_grid_with_drunken_walks_path(self):
        self.update_grid_with_new_path()
        self.update_grid_with_rooms()
        self.update_grid_with_walls()
        self.upgrade_grid_with_stair()
        self.is_done_generating = True
        