# Запускать это

import pygame
import sys
from main_screen import MainScreen
from start_screen import StartScreen

class Game:
    def __init__(self, size: tuple[int, int]) -> None:
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h - 128
        #self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.set_mode((640, 538))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("ПД")
        self.menu_screen()

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
            main_screen.draw(self.screen)
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
            self.clock.tick(self.FPS)
            pygame.display.flip()

    def terminate(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game((1200, 900))
