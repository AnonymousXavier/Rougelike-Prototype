from src.Misc.Spritesheet import SpriteSheet
from src.Globals import Enums
from src.Globals import Stats
import pygame

class Sprites:
    class Heroes:
        Green_Ninja = SpriteSheet(pygame.image.load("Assets/Player/Green Ninja.png"), (1, 4))
        ALL = {
            Enums.HEROES.GREEN_NINJA: Green_Ninja
        }

    class Tiles:
        wall = pygame.image.load("Assets/Tileset/wall.png")
        floor = pygame.image.load("Assets/Tileset/floor.png")
        pathway = pygame.image.load("Assets/Tileset/pathway.png")
        blank = pygame.image.load("Assets/Tileset/blank.png")
    
    class Enemies:
        cyclops = SpriteSheet(pygame.image.load("Assets/Enemies/Cyclops.png"), (1, 4))

        ALL = {
            Enums.ENEMIES.CYCLOPS: cyclops
        }

    class Facesets:
        Green_Ninja = pygame.transform.scale_by(pygame.image.load("Assets/Faceset/Cyclops.png"), 2)
        ALL = {
            Enums.HEROES.GREEN_NINJA: Green_Ninja
        }

    class Interactables:
        Chest = SpriteSheet(pygame.image.load("Assets/Interactables/smallChest.png"), (1, 2))
        Bush = SpriteSheet(pygame.image.load("Assets/Interactables/bush.png"), (1, 2))

    class Consumables:
        Potion = pygame.image.load("Assets/Items/HealthPotion.png")
        Nut = pygame.image.load("Assets/Items/Nut.png")
        ALL = {
            Enums.CONSUMABLES.POTION: Potion,
            Enums.CONSUMABLES.NUT: Nut,
        }

class Stats_Info:
    Heroes = {
        Enums.HEROES.GREEN_NINJA: Stats.ALL_STATS.GREEN_NINJA
    }
    Enemies = {
        Enums.ENEMIES.CYCLOPS: Stats.ALL_STATS.CYCLOPS
    }
    Consumables = {
        Enums.CONSUMABLES.POTION: Stats.ALL_STATS.POTION,
        Enums.CONSUMABLES.NUT: Stats.ALL_STATS.NUT
    }


