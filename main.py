import pygame
import sys
import random
from src.Misc import Save_Data
from src.Misc.level_transition import Level_Transition
from src.Core.HUD import HUD
from src.Core.Menu.menu import Menu
from src.Core.World import World
from src.Globals import settings, Cache
import src.Misc.xml_func as xml

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
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

        self.change_game_music()

    def change_game_music(self):
        # Choose a random music after fading out 
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(1000)

        music_path = ""
        match self.state:
            case State.START:
                music_path = random.choice(Cache.Audio.Music_Path.START)
            case State.GAME:
                music_path = random.choice(Cache.Audio.Music_Path.GAME)
            case State.GAME_OVER:
                music_path = random.choice(Cache.Audio.Music_Path.END)
        
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

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
        if settings.PLAY_SOUND:
            Cache.Audio.Sound.NEXT_FLOOR.play()

        
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
        xml.update(xml.load(settings.PATH))

    def update(self):
        dt = self.clock.tick(settings.FPS) / 150
        settings.DT = dt
        self.process_input()

        match self.state:
            case State.GAME:
                self.update_game(dt)
                self.update_transition(dt)
            case State.START:
                self.menu.update_start_menu()
            case State.GAME_OVER:
                self.menu.update_game_over_menu()
                self.update_transition(dt)

        self.manage_states()

        if not settings.PLAY_MUSIC:
            pygame.mixer.music.stop()
        if not pygame.mixer.music.get_busy() and settings.PLAY_MUSIC:
            self.change_game_music()

        pygame.display.update()

    def reset(self):
        self.world = World()
        self.hud = HUD(self.world)
        self.menu = Menu(self.world)

    def manage_states(self):
        match self.state:
            case State.GAME:
                if self.world.player.health < 0:
                    if settings.PLAY_SOUND:
                        Cache.Audio.Sound.GAME_OVER.play()
                    self.state = State.GAME_OVER
                    self.level_transition_animation.start()
                    self.change_game_music()
            case State.START:
                if self.menu.start_game:
                    Cache.Audio.Sound.START_GAME.play()
                    self.state = State.GAME
                    self.change_game_music()
            case State.GAME_OVER:
                if self.menu.return_to_menu:
                    self.state = State.START
                    self.change_game_music()
                    self.reset()


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
        frame = 0
        while True:
            if frame % 2 == 0: 
                self.update()
                self.draw()
            frame += 1

Main().run()
