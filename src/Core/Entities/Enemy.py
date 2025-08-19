from src.Misc.Spritesheet import SpriteSheet
from src.Globals.Cache import Sprites, Stats_Info
from src.Core.Entities.Entities import Entities

class Enemy(Entities):
    def __init__(self, id: int):
        self.spriteSheet: SpriteSheet = Sprites.Enemies.ALL[id]
        super().__init__(self.spriteSheet.image, self.spriteSheet.get_frames()[0], Stats_Info.Enemies[id])

    def update(self, grid_map: list):
        self.update_direction(grid_map)

    
            
