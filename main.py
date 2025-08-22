import pygame
import sys
from src.Misc import Save_Data
from src.Misc.level_transition import Level_Transition
from src.Core.HUD import HUD
from src.Core.Menu.menu import Menu
from src.Core.World import World
import src.Globals.settings as settings
import src.Misc.xml_func as xml

pygame.display.set_caption(f"{settings.GAME_NAME} v{settings.VERSION}")

#TODO:
# Core
# -> Enemy Levels Increase with Floor Levels -----------------------------------------DONE
# -> Player Buff Upgrades (1 pt per upgrade - Health or Damage) ----------------------DONE
    # Will be Included with Options Menu (Sound, Music, Quit and Version)
    # Pressing Esc will bring up this menu
# -> Add a main menu with
    # Player Customizations - Name and Skin (Same Menu) then Play
    # Credits screen with ninja Andventure Assets Pack Image
# -> Add Enemies Count

# Quality
# -> 2 More Enemies
# -> 2 More Loot types
# -> Make Consumables have Rarity for balancing Issues
# -> Save and load feauture with XML

class State:
    START= 0
    GAME = 1
    GAME_OVER = 2

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode(settings.SCREEN_SIZE, pygame.RESIZABLE)
        self.clock = pygame.Clock()
        self.world = World()
        self.hud = HUD(self.world)

        self.load_game()
        self.menu = Menu(self.world)
        self.level_transition_animation = Level_Transition()
        self.state = State.START

    def manage_input_processing(self, event: pygame.Event):
        match self.state:
                case State.GAME:
                    self.process_game_input(event)
            
    def process_game_input(self, event: pygame.Event):
        if self.level_transition_animation.complete:
            self.world.process_input(event)
            self.hud.process_input(event)

    def move_to_next_floor(self):
        player = self.world.player

        self.world = World(self.world.current_room_count + 1)

        self.world.player = player
        self.world.hud = self.hud
        self.hud.world = self.world

        self.level_transition_animation.start()
        
    def draw_game(self):
        if self.level_transition_animation.finish_growing:
            self.world.draw()
            self.hud.draw()

    def update_game(self, dt):

        if self.world.ready_to_move_to_next_floor:
            self.move_to_next_floor()

        self.hud.update(dt)
        self.hud.current_fps = self.clock.get_fps()

        self.process_input()
        self.world.update(dt)

    def update_transition(self, dt: float):
        if not self.level_transition_animation.complete:
            self.level_transition_animation.update(dt)

    def draw_transition(self):
        if not self.level_transition_animation.complete:
            self.level_transition_animation.draw(self.window)

    def process_input(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                xml.save(settings.PATH)
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                if self.state != State.GAME:
                    settings.SCREEN_WIDTH = event.w
                    settings.SCREEN_HEIGHT = event.h

                    settings.update_constants()
                    self.world = World()
                    self.hud = HUD(self.world)
                    self.menu = Menu(self.world)
                else:

                    pygame.display.set_mode(settings.SCREEN_SIZE)

            self.manage_input_processing(event)

    def load_game(self):
        print(xml.load(settings.PATH))
        if xml.load(settings.PATH):
            xml.update(xml.load(settings.PATH))
        else:
            Save_Data.reset()
            xml.save(settings.PATH)

    def update(self):

        dt = self.clock.tick(settings.FPS) / 100
        self.process_input()

        match self.state:
            case State.GAME:
                self.update_game(dt)
                self.update_transition(dt)
            case State.START:
                self.menu.update()
            case State.GAME_OVER:
                self.update_transition(dt)

        self.manage_states()
        pygame.display.update()

    def manage_states(self):
        match self.state:
            case State.GAME:
                if self.world.player.health < 0:
                    self.state = State.GAME_OVER
                    self.level_transition_animation.start()
            case State.START:
                if self.menu.start_game:
                    self.state = State.GAME


    def draw(self):
        self.window.fill((0, 0, 0))

        match self.state:
            case State.GAME:
                self.draw_game()
                self.draw_transition()
            case State.START:
                self.menu.draw_start_screen(self.window)
            case State.GAME_OVER:
                if self.level_transition_animation.finish_growing:
                    self.menu.draw_end_menu(self.window)
                self.draw_transition()


    def run(self):
        while True:
            self.update()
            self.draw()

Main().run()
