import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera_offset_x):
        pass
        # pygame.draw.rect(screen, (0, 0, 0), self.rect.move(-camera_offset_x, 0))