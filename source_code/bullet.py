import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))  # Placeholder image
        self.image.fill((255, 0, 0))  # Green circle for now
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 10 if direction == "right" else -10  # Set velocity based on direction

    def update(self):
        self.rect.x += self.vel_x