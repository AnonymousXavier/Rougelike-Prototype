import pygame


def calculate_cell_size(screen_width, grid_rows, cell_spacing):
    return (screen_width / (grid_rows + 1)) - cell_spacing

def calculate_grid_size(cell_width, cell_spacing, grid_cols):
    return (cell_width + cell_spacing) * grid_cols

def clamp(value: float, minValue: float, maxValue: float):
    if value > maxValue: 
        return maxValue
    if value < minValue: 
        return minValue
    return value

def clone_2D_array(array: list[list]):
    return [ row.copy() for row in array]

def sign(value):
    return -1 if value < 0 else 1

def fill_text(goal_width: int, *words:str):
    total_words_lenght = sum([len(word) for word in words])
    spacing = int((goal_width - total_words_lenght) / (len(words) - 1))

    filled_text = ""
    for word in words:
        filled_text = filled_text + word + " " * spacing
    return filled_text

def get_vector_magnitude(vec):
    x, y = vec
    return (x ** 2 + y ** 2) ** 0.5

def calculate_xp_gain_from_kill(enemy, player):
    bonus_xp_perc = 0.1 
    
    level_diff = enemy.level - player.level
    xp = enemy.max_health / enemy.level 

    return xp + level_diff * xp * bonus_xp_perc

def create_sprite(size: tuple[float, float], sheet: pygame.Surface, frame: pygame.Rect):
    sprite = pygame.Surface(size, pygame.SRCALPHA)
    sprite.blit(sheet, (0,0), frame)

    return sprite

def get_grid_size(grid: list[list]):
    grid_height = len(grid) - 1
    grid_width = len(grid[0]) - 1

    return grid_width, grid_height

def rotate_surface(surface, angle):
    surface.set_colorkey((0, 0, 0))
    temp_surface = surface
    temp_surface_rect = temp_surface.get_rect(topleft = (0, 0))

    rotated_surface = pygame.transform.rotate(surface, angle)
    desired_surface = pygame.Surface(rotated_surface.size, pygame.SRCALPHA)

    desired_surface.blit(rotated_surface, rotated_surface.get_rect(center=temp_surface_rect.center))
    return desired_surface

def wrap_text(text: str, max_line_lenght: int):
    wrapped_text_list: list[str] = []
    seperated_text = text.split(" ")

    line_text = ""    
    for word in seperated_text:
        line_lenght = len(line_text) + len(word)
        if line_lenght <= max_line_lenght:
            if line_text == "":
                line_text = word
            else:
                line_text = line_text + " " + word
        else:
            wrapped_text_list.append(line_text)
            line_text = word

    wrapped_text_list.append(line_text)
    
    return wrapped_text_list

def get_font(name: str, font_size: int, is_bold=False, is_italic=False) -> pygame.Font:
    return pygame.font.SysFont(name, font_size, is_bold, is_italic)

