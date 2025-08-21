class World_Types:
    WALL = 0
    FLOOR = 1
    DOOR = 2
    BLANKS = 3 
    STAIR = 4
    ALL = (WALL, FLOOR, DOOR, BLANKS)

class SPRITE_INDEX:
    DOWN = 0
    UP = 1
    LEFT = 2
    RIGHT = 3
    ALL = (UP, DOWN, LEFT, RIGHT)

class DIRECTIONS:
    DOWN = (0, 1)
    UP = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    ALL = (DOWN, LEFT, RIGHT, UP)

class INTERACTABLES_STATES:
    OPEN = 1
    CLOSED = 0

class ITEM_TYPES:
    CONSUMABLES = 0
    LOOT = 1

class CONSUMABLES:
    POTION = 0
    NUT = 1
    CALAMARI = 2
    BEEF = 3
    ALL = (POTION, NUT, CALAMARI, BEEF)

class ENEMIES:
    CYCLOPS = 0

class HEROES:
    GREEN_NINJA = 0

class RARITY:
    COMMON = 1
    RARE = 2
    EPIC = 3
    LENGENDARY = 4