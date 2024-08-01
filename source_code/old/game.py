# Запускать это
# todo: https://github.com/MyreMylar/pygame_gui_examples https://github.com/Grimmys/rpg_tactical_fantasy_game
import pygame
import pygame_gui
import sys
from main_screen import MainScreen
from portal_screen import PortalScreen
from start_screen import StartScreen
from world_screen import WorldScreen

class Game:
    def __init__(self, size: tuple[int, int]) -> None:
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h - 128
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.screen = pygame.display.set_mode((640, 538))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ПД")
        self.world_screen()

    def menu_screen(self):
        running = True
        main_screen = MainScreen(self.screen)
        while running:
            self.screen.fill(pygame.Color('#d87093'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    self.game_screen()
            main_screen.update()
            main_screen.draw()
            self.clock.tick(self.FPS)
            pygame.display.flip()

    def game_screen(self):
        running = True
        start_screen = StartScreen(self, self.screen)
        while running:
            self.screen.fill(pygame.Color('#f37153'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.terminate()
            start_screen.update(pygame.event.get())
            start_screen.draw(self.screen)
            if start_screen.portal_touched:
                running = False
                self.portal_screen()
            self.clock.tick(self.FPS)
            pygame.display.flip()
    
    def portal_screen(self):
        running = True
        portal_screen = PortalScreen(self.screen)
        while running:
            self.screen.fill(pygame.Color('#d87093'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.terminate()
            portal_screen.update()
            portal_screen.draw(self.screen)
            self.clock.tick(self.FPS)
            pygame.display.flip()
            
    def world_screen(self):
        running = True
        world_screen = WorldScreen(self, self.screen)
        while running:
            self.screen.fill(pygame.Color('#d87093'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.terminate()
            world_screen.update(pygame.event.get())
            
            world_screen.draw(self.screen)
            self.clock.tick(self.FPS)
            pygame.display.flip()
    
    def terminate(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game((1200, 900))
