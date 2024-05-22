import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, texture):
        super().__init__()
        self.image = texture
        self.rect = pygame.Rect(x, y, width, height)
        self.texture = texture
        self.selected = False

    def draw(self, screen, camera_offset_x):
        if not self.selected:
            screen.blit(self.image, ((self.rect.x - camera_offset_x, self.rect.y)))
        else:
            texturee = pygame.image.load("resources/textures/blocks/selected.png").convert_alpha()
            texture = pygame.transform.scale(texturee, (50, 50))
            screen.blit(texture, ((self.rect.x - camera_offset_x, self.rect.y)))

    def handle_collision(self, player):
        if self.rect.colliderect(player.rect):
            print('colis')
            self.selected = not self.selected

class MathBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/math.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)

class PhysicsBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/physics.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)

class BiologyBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/biology.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)
        

class ChemistryBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/chemistry.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)

class CodingBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/coding.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)

class GeographyBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/geography.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)
        
class LanguageBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/language.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)
        
class LiteratureBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/literature.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)
        
class RussianBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/russian.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)
        
class SocialBox(Box):
    def __init__(self, x, y):
        texturee = pygame.image.load("resources/textures/blocks/social.png").convert_alpha()
        texture = pygame.transform.scale(texturee, (50, 50))
        super().__init__(x, y, 50, 50, texture)