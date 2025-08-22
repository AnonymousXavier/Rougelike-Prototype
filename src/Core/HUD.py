import pygame
from src.UI.options_menu import Options_Menu
from src.UI.Active_Buffs_HUD import Active_Buff_HUD_Display
from src.UI.Player_stats_hud import Player_Stats_HUD
from src.UI.Player_HUD import Player_HUD_Display
from src.UI.enemy_info_display_component import Enemy_Info_Display_Component
from src.UI.Inventory_Display import Inventory_Display
from src.UI.label import Label
from src.Globals import settings
from src.Misc import Misc
from src.Core.World import World


class HUD:
    def __init__(self, world: World):
        self.world = world
        self.world.hud = self
        self.window = world.window
        self.surface = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)

        # Misc
        self.current_fps = 0.0
        self.alpha: int  = 255
        self.fade_speed = 15

        # Player 
        self.can_display_inventory = False
        self.options_menu = Options_Menu()
        self.player_hud_display = Player_HUD_Display(self.world.player)
        self.inventory_display_hud = Inventory_Display(self.world.player)
        self.player_stats_hud = Player_Stats_HUD(self.world.player)
        self.player_active_buff_display = Active_Buff_HUD_Display(self.world.player)

        # Enemy HUD Components
        self.enemy_info_display_components: list[Enemy_Info_Display_Component] = []

        # Info Labels
        self.fps_label = Label("60", settings.FPS_INFO_SIZE)
        self.fps_label.font_color = settings.Color.DARKER_GREY
        self.enemies_in_floor_label = Label("Enemies: 0/0", settings.FPS_INFO_SIZE)
        self.enemies_in_floor_label.font_color = settings.Color.DARKER_GREY

        # Bottom Center Floor Count
        self.floor_label = Label("FLOOR 0", settings.FPS_INFO_SIZE)
        self.floor_label.font_color = self.fps_label.font_color
    
    def draw(self):
        self.surface = pygame.Surface(settings.SCREEN_SIZE, pygame.SRCALPHA)
        self.surface.set_alpha(self.alpha)

        self.player_hud_display.draw(self.surface)
        self.update_info_labels()
        self.draw_enemy_inrange_info()

        self.inventory_display_hud.draw(self.surface)
        self.player_stats_hud.draw(self.surface)
        self.player_active_buff_display.draw(self.surface)
        self.options_menu.draw(self.surface)

        self.window.blit(self.surface)

    def draw_enemy_inrange_info(self):
        for enemy_info in self.enemy_info_display_components:
            enemy_info.draw(self.surface)


    def update_enemy_inrange_info_with_new_ones(self, dt: float):
        self.enemy_info_display_components = []

        tx, ty = self.player_hud_display.hud_panel.rect.topright # Top Left
        sw = settings.ENEMY_INFO_SIZE[0]

        tx, ty = tx + settings.SCREEN_MARGIN, ty + settings.SCREEN_MARGIN
        
        remaining_width = (settings.SCREEN_WIDTH - tx)
        section_width = (remaining_width - sw) / 3

        n = 3
        
        for enemy in self.world.get_attackable_enemies():
            enemy_info = Enemy_Info_Display_Component(settings.ENEMY_INFO_SIZE)

            enemy_info.title_label.text = Misc.fill_text(14, enemy.name, f"LVL {enemy.level}")
            enemy_info.health_bar.value = enemy.health
            enemy_info.health_bar.maxValue = enemy.max_health
            enemy_info.dmg_label.text = f"DMG: {enemy.damage}"

            enemy_info.rect.topleft = tx + section_width * n, ty
            enemy_info.update(dt)

            self.enemy_info_display_components.append(enemy_info)

            n -= 1

    def update_exisiting_enemy_inrange_info(self, dt: float):
        attacking_enemies = self.world.get_attackable_enemies()
        for i, enemy_info in enumerate(self.enemy_info_display_components):
            enemy = attacking_enemies[i]

            enemy_info.title_label.text = Misc.fill_text(14, enemy.name, f"LVL {enemy.level}")
            enemy_info.health_bar.value = enemy.health
            enemy_info.health_bar.maxValue = enemy.max_health

            enemy_info.update(dt)

    def update_enemy_inrange_info(self, dt: float):
        if len(self.world.get_attackable_enemies()) == len(self.enemy_info_display_components):
            self.update_exisiting_enemy_inrange_info(dt)
        else: 
            self.update_enemy_inrange_info_with_new_ones(dt)

    def update_info_labels(self):
        self.fps_label.text = str(round(self.current_fps))
        self.fps_label.update()
        self.fps_label.rect.bottomleft = (settings.SCREEN_MARGIN, settings.SCREEN_HEIGHT - settings.SCREEN_MARGIN)
        
        self.floor_label.text = f"FLOOR {self.world.floor}"
        self.floor_label.update()
        self.floor_label.rect.midbottom = settings.SCREEN_CENTER[0], self.fps_label.rect.bottom

        self.enemies_in_floor_label.text = f"Enemies: {self.world.enemies_data.alive}/{self.world.enemies_data.total}"
        self.enemies_in_floor_label.update()
        self.enemies_in_floor_label.rect.topleft = self.fps_label.rect.left, self.player_hud_display.faceset_rect.bottom + settings.SCREEN_MARGIN

        self.floor_label.draw(self.surface)
        self.fps_label.draw(self.surface)
        self.enemies_in_floor_label.draw(self.surface)

    def update_draw_surface_alpha(self, dt: float):
        is_overlaping = (self.world.player.rect.top - 32) <= 0
        target_alpha = 100 if is_overlaping else 255

        diff = target_alpha - self.alpha 
        self.alpha += int(min(dt * self.fade_speed, abs(diff)) * Misc.sign(diff))

    def update(self, dt: float):
        self.update_draw_surface_alpha(dt)
        self.player_hud_display.update(dt)

        if self.world.finished_initializing: 
            self.update_enemy_inrange_info(dt)

        self.inventory_display_hud.update(dt)
        self.options_menu.update()
        self.player_stats_hud.update()

        if self.world.should_update_game():
            self.player_active_buff_display.update()

    def process_input(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN and event.key == settings.Controls.INVENTORY:
            self.inventory_display_hud.visible = not self.inventory_display_hud.visible
            self.player_stats_hud.visible = not self.player_stats_hud.visible
        if event.type == pygame.KEYDOWN and event.key == settings.Controls.OPTIONS:
            self.options_menu.visible = not self.options_menu.visible 


        self.inventory_display_hud.process_input(event)
        self.player_stats_hud.process_input(event)
        self.options_menu.process_input(event)

        