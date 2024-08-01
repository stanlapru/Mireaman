import pygame

class LessonBox(pygame.sprite.Sprite):
    def __init__(self, x,y, width, height, texture, id, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(pygame.image.load(texture), (width, height))
        self.rect = self.image.get_rect()
        self.texture = texture
        self.selected = False
        self.id = id
        self.rect = self.rect.move(x,y)

    def handle_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.selected = not self.selected