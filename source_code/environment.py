import pygame
from platform2 import Platform
from portal import Portal
from source_code.lesson_box import MathBox


class Environment:
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()

    def add_platform(self, x, y, width, height):
        platform = Platform(x, y, width, height)
        self.platforms.add(platform)
        
    def add_box(self, x, y):
        box = MathBox(x, y,)
        self.boxes.add(box)
        
    def add_box2(self, x, y,):
        box = PhysicsBox(x, y)
        self.boxes.add(box)
        
    def add_box3(self, x, y,):
        box = LanguageBox(x, y, )
        self.boxes.add(box)
        
    def add_box4(self, x, y,):
        box = LiteratureBox(x, y,)
        self.boxes.add(box)

    def add_box5(self, x, y, ):
        box = GeographyBox(x, y, )
        self.boxes.add(box)

    def add_box6(self, x, y, ):
        box = SocialBox(x, y, )
        self.boxes.add(box)
        
    def add_box7(self, x, y, ):
        box = RussianBox(x, y, )
        self.boxes.add(box)
        
    def add_box8(self, x, y, ):
        box = CodingBox(x, y, )
        self.boxes.add(box)
        
    def add_box9(self, x, y, ):
        box = ChemistryBox(x, y, )
        self.boxes.add(box)
        
    def add_box10(self, x, y, ):
        box = BiologyBox(x, y, )
        self.boxes.add(box)
        
    def draw(self, surface):
        self.platforms.draw(surface)
        self.boxes.draw(surface)