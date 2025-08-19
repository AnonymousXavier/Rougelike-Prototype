class Entity_Stat:
	def __init__(self, name, health: float, damage: float):
		self.name = name
		self.health = health
		self.damage = damage

class Item_Stat:
	def __init__(self, name, description: str):
		self.description = description
		self.name = name

class ALL_STATS:
	# Heroes
	GREEN_NINJA = Entity_Stat("Green Ninja", 25, 2)
	# Enemies
	CYCLOPS = Entity_Stat("Cyclops", 3, 1)
	# Consumables
	POTION = Item_Stat("Potion", "Heals 10% of health")
	NUT = Item_Stat("Nut", "Heals by 10 health points")

