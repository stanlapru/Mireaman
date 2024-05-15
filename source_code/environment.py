import pygame
from platform import Platform

class Environment:
    def __init__(self):
        self.platforms = pygame.sprite.Group()

    def add_platform(self, x, y, width, height):
        platform = Platform(x, y, width, height)
        self.platforms.add(platform)

    def draw(self, surface):
        self.platforms.draw(surface)