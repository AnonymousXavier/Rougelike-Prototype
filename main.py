import pygame
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

    def process_input(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                quit()
            self.world.process_input(event)
            self.hud.process_input(event)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.world.draw()
        self.hud.draw()

    def update(self):
        dt = self.clock.tick(settings.FPS) / 100

        self.process_input()
        self.world.update(dt)
        self.hud.update(dt)
        self.hud.current_fps = self.clock.get_fps()

        pygame.display.update()

    def run(self):
        while True:
            self.update()
            self.draw()


Main().run()
