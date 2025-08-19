from src.Core.Items.Consumable import Item

class Inventory:
	def __init__(self):
		# Items are indexed by their object and their count is returned
		self.items: dict[str, list[Item]] = {}

	def add(self, obj):
		if isinstance(obj, Item):
			obj_name = obj.name

			if obj_name in self.items:
				self.items[obj_name].append(obj)
			else:
				new_type_list = []
				new_type_list.append(obj)
				self.items[obj_name] = new_type_list

	def remove(self, obj):
		if isinstance(obj, Item):
			obj_name = obj.name

			if obj_name in self.items:
				if obj in self.items[obj_name]:
					self.items[obj_name].remove(obj)
					if self.items[obj_name] == []: 
						del self.items[obj_name]
					return True
		return False

	def __repr__(self):
		msg = ""
		for key in self.items:
			msg = msg + f"{key}: {self.items[key]}\n"
		return msg
