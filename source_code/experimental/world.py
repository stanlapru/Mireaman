import pygame
import pygame_gui
from support import *
from tile import *
from world import *
from player import *

class World:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./resources/tmx/map_collision.csv'),
            'decorations1': import_csv_layout('./resources/tmx/map_softdecorations1.csv'),
            'decorations2': import_csv_layout('./resources/tmx/map_softdecorations2.csv'),
            'decorations3': import_csv_layout('./resources/tmx/map_softdecorations3.csv'),
            'solids1': import_csv_layout('./resources/tmx/map_harddecorations1.csv'),
            'solids2': import_csv_layout('./resources/tmx/map_harddecorations2.csv'),
        }
        graphics = {
            'overworld': import_folder('./resources/tmx/tsx/Overworld')
        }

        for style,layout in layouts.items():
            for row_idx,row in enumerate(layout):
                for col_idx,col in enumerate(row):
                    if col != '-1':
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        # if style == 'decorations1' or style == 'decorations2' or style == 'decorations3':
                        #     Tile((x,y), [self.visible_sprites], 'walkable')
                        # if style == 'solids1' or style == 'solids2':
                        #     Tile((x,y), [self.visible_sprites], 'solid')
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        self.player = Player((1200,1300),[self.visible_sprites], self.obstacle_sprites)
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
class YSortCamGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.floor_surface = pygame.image.load("./resources/textures/environment/world_big.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
            