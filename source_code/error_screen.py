import pygame
from pygame.locals import *

class ErrorScreen:
    def __init__(self, game: pygame.Surface, clock, error):
        self.game = game
        pygame.mixer.init()
        pygame.mixer.music.stop()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.clock = clock
        self.error = error
        self.texts = []
        self.initialize_error()

    def initialize_error(self):
        error_list = error_list = ["RUNTIME ERROR! Please restart!",'',"--- Exception Details ---",self.error]
        for i, line in enumerate(error_list):
            s = self.font.render(line, 1, (255, 255, 255))
            r = s.get_rect(x=self.game.get_rect().left, y=self.game.get_rect().top + i * 45)
            self.texts.append((r, s))
            
    def draw(self):
        self.game.fill(pygame.Color('#0000bb'))
        
        for r, s in self.texts:
            self.game.blit(s, r)

        self.clock.tick(60)