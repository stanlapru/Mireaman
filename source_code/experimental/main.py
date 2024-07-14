# LAUNCH THIS
import pygame
import pygame_gui
import subprocess
import threading
import sys
from settings import *
from world import *


class Game:
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мир грифонов")
        
        # Custom cursor
        cursor_surface = pygame.image.load('./resources/textures/cursor/Tiles/tile_0049.png')
        cursor_surface_32x32 = pygame.transform.scale(cursor_surface, (32, 32))
        hotspot = (0, 0)
        cursor = pygame.cursors.Cursor(hotspot, cursor_surface_32x32)
        pygame.mouse.set_cursor(cursor)
        
        self.clock = pygame.time.Clock()
        self.world = World()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.fill('black')
            self.world.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
            
if __name__ == "__main__":
    game = Game()
    game.run()
