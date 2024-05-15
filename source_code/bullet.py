import pygame
import os
import sys

def load_image(name, colokey=None):
    fullname = os.path.join('resources/textures', name)
    if not os.path.isfile(fullname):
        print('not found', fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colokey is not None:
        image = image.convert()
        if colokey == -1:
            colokey = image.get_at((0, 0))
        image.set_colorkey(colokey)
    return image 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = load_image('projectiles/p_shooter.png')
        #self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 10 if direction == "right" else -10  # Set velocity based on direction

    def update(self):
        self.rect.x += self.vel_x
        