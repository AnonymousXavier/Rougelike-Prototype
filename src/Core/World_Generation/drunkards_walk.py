import random
import pygame
from src.Misc.Cell import Cell
import src.Globals.settings as settings

random.seed(1)

class Drunkards_Walk:
    def __init__(self, max_steps: int):
        self.taken_cells: list[Cell] = []
        self.chosen_start_positions = []

        self.update_ticks_delay = 0
        self.last_tick = 0
        self.ticks = 0
        self.max_steps = max_steps

        self.grid = self.create_grid()
        self.drop_drunkard()

    def drop_drunkard(self):
        i = random.randint(0, settings.GRID_ROWS - 1)
        j = random.randint(0, settings.GRID_COLS - 1)
        
        if (i, j) in self.chosen_start_positions: return self.drop_drunkard()

        cell = self.grid[i][j]
        cell.is_taken = True
        self.taken_cells.append(cell)

        self.chosen_start_positions.append((i, j))

        print("Drunkard Spanwed")
        print("Start Positions: ", self.chosen_start_positions)

    def reset_grid(self):
        self.grid = self.create_grid()
        self.taken_cells = []
        self.drop_drunkard()

    def create_grid(self) -> list[list[Cell]]:
        grid = []
        for i in range(settings.GRID_ROWS):
            row = []
            for j in range(settings.GRID_COLS):
                cell = Cell(i, j)
                row.append(cell)
            grid.append(row)
        return grid
    
    def has_reached_max_steps(self) -> bool:
        return len(self.taken_cells) >= self.max_steps

    def draw_grid(self, surface: pygame.Surface):
        temp_surface = pygame.Surface((settings.GRID_WIDTH, settings.GRID_HEIGHT))
        temp_surface_rect = temp_surface.get_rect(center=settings.SCREEN_CENTER)

        for cell in self.taken_cells:
            cell.draw(temp_surface)
        
        self.draw_direction_lines(temp_surface)
        surface.blit(temp_surface, temp_surface_rect)

    def draw(self, surface: pygame.Surface):
        self.draw_grid(surface)

    def draw_direction_lines(self, surface: pygame.Surface):
        x1, y1 = self.taken_cells[0].cx, self.taken_cells[0].cy

        for cell in self.taken_cells:
            x2, y2 = cell.cx, cell.cy
            pygame.draw.line(surface, settings.CONNECTING_LINE_COLOR, (x1, y1), (x2, y2))
            x1, y1 = x2, y2

    def is_out_of_bounds(self, step: tuple[int, int]):
        r, c = step

        if r >= len(self.grid) or c >= len(self.grid[0]): return True
        if r < 0 or c < 0: return True
        return False

    def is_stuck(self, cell: Cell):
        return len(cell.options) == 0

    def backtrack_last_move(self):
        last_step = self.taken_cells[len(self.taken_cells) - 1]
        prev_step = self.taken_cells[len(self.taken_cells) - 2]

        dx, dy = last_step.c - prev_step.c, last_step.r - prev_step.r

        option_id = prev_step.get_option_index((dx, dy))
        print(prev_step.options, (dx, dy), option_id)
        if option_id >= 0:
            print("removing: ", (dx, dy) ," from ", prev_step.options, "(Backtracking)")
            prev_step.options.remove(prev_step.options[option_id])
        
        self.taken_cells.remove(last_step)
        self.grid[last_step.r][last_step.c].is_taken = False

    def has_filled_grid(self):
        return len(self.taken_cells) == settings.GRID_COLS * settings.GRID_ROWS

    def update_drunken_man(self):
        if self.has_reached_max_steps(): return

        if self.has_filled_grid(): return

        if not self.taken_cells: 
            print("Empty")
            return self.reset_grid()
        last_step = self.taken_cells[len(self.taken_cells) - 1]

        if self.is_stuck(last_step):
            # Backtrack last move
            # If this move made us stop, go to the last move and remove so it'll never do it again
            self.backtrack_last_move()
            print("No Options: Attempting to Backtrack by removing last move")
            return self.update_drunken_man()

        i, j = last_step.r, last_step.c           
        chosen_option = random.choice(last_step.options)
        dx, dy = chosen_option
        next_i, next_j = i + dy, j + dx

        if not self.is_out_of_bounds((next_i, next_j)):
            next_step = self.grid[next_i][next_j]
            if not next_step.is_taken:
                next_step.is_taken = True
                self.taken_cells.append(next_step)
                return 
        else:
            option_id = last_step.get_option_index((dx, dy))
            if option_id >= 0:
                print("removing: ", (dx, dy) ," from ", last_step.options, " (Out of Bounds)")
                last_step.options.remove(last_step.options[option_id])
                return
        
        last_step.options.remove(chosen_option)

        self.update_drunken_man()

    def can_update(self) -> bool:
        if self.ticks >= self.update_ticks_delay:
            self.ticks = 0
            return True
        return False

    def update(self, dt):
        self.ticks += dt / 100

        if self.can_update():
            self.update_drunken_man()