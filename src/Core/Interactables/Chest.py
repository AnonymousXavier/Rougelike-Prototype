import random
from src.Globals import Cache
from src.Core.Interactables.Interactables import Interactable
from src.Core.Items.Consumable import Consumable
from src.Globals import Enums


class Chest(Interactable):
    def __init__(self):
        self.spriteSheet = Cache.Sprites.Interactables.Chest
        super().__init__(self.spriteSheet.image, self.spriteSheet.get_frames()[0])

        # Always has loot
        self.spawn_consumable_loot(Enums.CONSUMABLES.ALL)

    def spawn_consumable_loot(self, item_ids: tuple):
        for _ in range(self.rarity):
            item_id = random.choice(item_ids)
            self.content.append(Consumable(item_id))