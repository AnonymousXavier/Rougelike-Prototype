from src.Globals import Cache
from src.Globals import Enums
from src.Core.Items.Item import Item
from src.Globals.Cache import Sprites, Stats_Info
from src.Misc import Misc

class Consumable(Item):
    def __init__(self, consumable_id: int):
        self.image = Sprites.Consumables.ALL[consumable_id]
        super().__init__(self.image, [self.image.get_rect()], Stats_Info.Consumables[consumable_id])

        self.id = consumable_id
        self.rect = self.image.get_rect()

    def use(self, player):
        match self.id:
            case Enums.CONSUMABLES.POTION:
                player.health = Misc.clamp(player.health + player.get_max_health() * 0.2, 0, player.get_max_health())
            case Enums.CONSUMABLES.NUT:
                player.health = Misc.clamp(player.health + 10, 0, player.get_max_health())
            case Enums.CONSUMABLES.BEEF | Enums.CONSUMABLES.CALAMARI:
                calamari_buff = Cache.Consumable_Buff(self.id, self.effect_duration)
                player.passive_buffs.append(calamari_buff)
        Cache.Audio.Sound.ITEM.play()

            
