import pygame

class PlatformCollision(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, *group):
        super().__init__(*group)
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def handle_collision(self, player):
        # No collision handling needed for this type of platform
        pass
