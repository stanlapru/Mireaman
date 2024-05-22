import pygame

class Portal:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("resources/textures/portal/portal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen, camera_offset_x):
        screen.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y))
        
    def handle_collision(self, player):
        if self.rect.colliderect(player.rect):
            print('colis')
            self.selected = not self.selected