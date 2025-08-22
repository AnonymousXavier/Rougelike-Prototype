class SaveData:
	kills = 0
	level = 1
	floor = 0
	health = 25
	damage = 2
	seed = 0

def reset():
	SaveData.kills = 0
	SaveData.level = 0
	SaveData.floor = 0
	SaveData.health = 25
	SaveData.damage = 2
	SaveData.seed = 0

def update(world):
	SaveData.kills = world.player.kills
	SaveData.level = world.player.level
	SaveData.floor = world.floor
	SaveData.health = world.player.max_health
	SaveData.damage = world.player.damage
	SaveData.seed = world.world_generator.seed

def display_data():
	print("Saved Data")
	print(f"Kills: {SaveData.kills}")
	print(f"Level: {SaveData.level}")
	print(f"Floor: {SaveData.floor}")
	print(f"Health: {SaveData.health}")
	print(f"Damage: {SaveData.damage}")
	print(f"Seed: {SaveData.seed}")