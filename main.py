import pygame
from src.Misc.level_transition import Level_Transition
from src.Core.HUD import HUD
from src.Core.World import World
import src.Globals.settings as settings

pygame.display.set_caption("Roguelike - Prototype: Day 4")


class Main:
    def __init__(self):
        self.window = pygame.display.set_mode(settings.SCREEN_SIZE)
        self.clock = pygame.Clock()
        self.world = World()
        self.hud = HUD(self.world)
        self.level_transition_animation = Level_Transition()

    def process_input(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                quit()
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
        print(f"Floor: {self.world.current_room_count - settings.INITIAL_ROOM_COUNT}")

    def draw(self):
        self.window.fill((0, 0, 0))
        self.world.draw()
        self.hud.draw()
        if not self.level_transition_animation.complete:
            self.level_transition_animation.draw(self.window)

    def update(self):
        dt = self.clock.tick(settings.FPS) / 100

        if self.world.ready_to_move_to_next_floor:
            self.move_to_next_floor()

        self.hud.update(dt)
        self.hud.current_fps = self.clock.get_fps()

        self.process_input()
        self.world.update(dt)

        if not self.level_transition_animation.complete:
            self.level_transition_animation.update(dt)

        pygame.display.update()

    def run(self):
        while True:
            self.update()
            self.draw()


Main().run()
