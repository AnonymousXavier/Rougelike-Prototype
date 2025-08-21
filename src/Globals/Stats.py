class Entity_Stat:
	def __init__(self, name, health: float, damage: float):
		self.name = name
		self.health = health
		self.damage = damage

class Item_Stat:
	def __init__(self, name, description: str, duration=0):
		self.description = description
		self.name = name
		self.effect_duration = duration # zero implies its instantaneous

class ALL_STATS:
	# Heroes
	GREEN_NINJA = Entity_Stat("Green Ninja", 25, 2)
	# Enemies
	CYCLOPS = Entity_Stat("Cyclops", 3, 1)
	# Consumables
	POTION = Item_Stat("Potion", "Heals 20% of health")
	NUT = Item_Stat("Nut", "Heals by 1 health points")
	CALAMARI = Item_Stat("Calamari", "Doubles Damage for 25 turns", 25)
	BEEF = Item_Stat("Beef", "Doubles Health for 25 turns", 25)


