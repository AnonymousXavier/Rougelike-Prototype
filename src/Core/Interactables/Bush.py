import random
from src.Globals import Cache, settings, Enums
from src.Core.Interactables.Interactables import Interactable
from src.Core.Items.Consumable import Consumable

class Bush(Interactable):
	def __init__(self):
		self.spriteSheet = Cache.Sprites.Interactables.Bush
		super().__init__(self.spriteSheet.image, self.spriteSheet.get_frames()[0])

		if random.randint(1, settings.BUSH_HAS_LOOT_CHANCE):
			self.spawn_consumable_loot(Enums.CONSUMABLES.ALL)

	def spawn_consumable_loot(self, item_ids: tuple):
		for _ in range(self.rarity):
			item_id = random.choice(item_ids)
			self.content.append(Consumable(item_id))

	def interact(self, player):
		super().interact(player)
		self.can_walk_over = True