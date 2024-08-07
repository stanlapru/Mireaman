import pygame, pytmx, pygame_gui
from settings import *
from support import *
from tile_platformer import *
from world import *
from player_platformer import *

#Background color
BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

#Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

class PlatformerWorld:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Kevin MacLeod - Cipher.mp3")
        pygame.mixer.music.play()
        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./resources/tmx/platformer/platformer_collision.csv'),
            'decorations': import_csv_layout('./resources/tmx/platformer/platformer_decorations.csv'),
            'solids': import_csv_layout('./resources/tmx/platformer/platformer_background.csv'),
        }
        graphics = {
            # 'overworld': import_folder('./resources/tmx/platformer/Assets/')
            'overworld': import_folder('./resources/tmx/tsx/Overworld/Overworld.png')
        }

        for style,layout in layouts.items():
            for row_idx,row in enumerate(layout):
                for col_idx,col in enumerate(row):
                    if col != '-1':
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        # tile_index = int(col)
                        # tile_surface = graphics['overworld'][tile_index]
                        if style == 'boundary':
                            TilePlatformer((x,y), [self.obstacle_sprites], 'tile_surface')
                        # if style == 'decorations1' or style == 'decorations2' or style == 'decorations3':
                        #     Tile((x,y), [self.visible_sprites], 'walkable')
                        # if style == 'solids1' or style == 'solids2':
                        #     Tile((x,y), [self.visible_sprites], 'solid')
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        self.player = PlayerPlatformer((1200,1300),[self.visible_sprites], self.obstacle_sprites)
    
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
        
        self.floor_surface = pygame.image.load("./resources/tmx/platformer/platformer.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
        
