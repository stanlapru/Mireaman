import pygame
import pygame_gui
from support import *
from tile import *
from world import *
from player import *

class World:
    def __init__(self, data, new):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = YSortCamGroup()
        self.foreground_sprites = ForegroundGroup()
        self.foreground_sprites_2 = ForegroundGroup()
        self.load_save = new
        
        self.data = data
        pygame.mixer.music.load("./resources/audio/music/Kevin MacLeod - Cipher.mp3")
        pygame.mixer.music.play()
        self.create_map()
        self.loaded = False
        
    def load_tileset(self, path, tile_size, scale_factor=3):
        tileset_image = pygame.image.load(path).convert_alpha()  # Load the tileset
        tiles = []

        # Calculate the number of tiles in the x and y directions
        sheet_width, sheet_height = tileset_image.get_size()
        tiles_x = sheet_width // tile_size[0]
        tiles_y = sheet_height // tile_size[1]

        # Loop through the tiles and extract each one
        for y in range(tiles_y):
            for x in range(tiles_x):
                rect = pygame.Rect(x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1])
                tile = tileset_image.subsurface(rect)  # Extract the tile using the rect

                # Scale the tile
                scaled_tile = pygame.transform.scale(tile, (tile_size[0] * scale_factor, tile_size[1] * scale_factor))
                tiles.append(scaled_tile)  # Add the scaled tile to the list

        return tiles
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./resources/tmx/map_collision.csv'),
            'decorations1': import_csv_layout('./resources/tmx/map_softdecorations1.csv'),
            'decorations2': import_csv_layout('./resources/tmx/map_softdecorations2.csv'),
            'decorations3': import_csv_layout('./resources/tmx/map_softdecorations3.csv'),
            'solids1': import_csv_layout('./resources/tmx/map_harddecorations1.csv'),
            'solids2': import_csv_layout('./resources/tmx/map_harddecorations2.csv'),
            'fore1': import_csv_layout('./resources/tmx/map_frontofplayer.csv'),
            'fore2': import_csv_layout('./resources/tmx/map_frontofplayer2.csv'),
        }
        
        graphics = {
            'overworld': self.load_tileset('./resources/tmx/tsx/Overworld.png', (16, 16), scale_factor=3)
        }

        for style,layout in layouts.items():
            for row_idx,row in enumerate(layout):
                for col_idx,col in enumerate(row):
                    if col != '-1':
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        tile_index = int(col)
                        if 0 <= tile_index < len(graphics['overworld']):
                            tile_surface = graphics['overworld'][tile_index]
                            if style == 'boundary':
                                Tile((x,y), [self.obstacle_sprites], tile_surface)
                            elif style == 'fore1':
                                Tile((x, y), [self.foreground_sprites], tile_surface)
                            elif style == 'fore2':
                                Tile((x, y), [self.foreground_sprites_2], tile_surface)
                            # elif style in ['decorations1', 'decorations2', 'decorations3']:
                            #     Tile((x, y), [self.visible_sprites], tile_surface)
                            # elif style in ['solids1', 'solids2']:
                            #     Tile((x, y), [self.visible_sprites], tile_surface)
                        else:
                            print(f"Invalid tile index {tile_index} at position ({row_idx}, {col_idx})")
        if self.load_save == True:
            self.player = Player((self.data['pos_x'],self.data['pos_y']),[self.visible_sprites], self.obstacle_sprites, self.data)
        else:
            self.player = Player((1200,1300),[self.visible_sprites], self.obstacle_sprites, self.data)
        self.visible_sprites.add(self.player)
        
        self.loaded = True

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.foreground_sprites.custdraw(self.player)
        self.foreground_sprites_2.custdraw(self.player)
        
class YSortCamGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.floor_surface = pygame.image.load("./resources/textures/environment/world_big.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
        self.visible_sprites = pygame.sprite.Group()
        
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        # player
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
            
        # visibles
        for sprite in sorted(self.visible_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
            
        # Draw foreground layers
        # for sprite in sorted(self.foreground_sprites, key=lambda sprite: sprite.rect.centery):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     self.display.blit(sprite.image, offset_pos)
        
        # for sprite in sorted(self.foreground_sprites_2, key=lambda sprite: sprite.rect.centery):
        #     offset_pos = sprite.rect.topleft - self.offset
        #     self.display.blit(sprite.image, offset_pos)

class ForegroundGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.foreground_sprites = pygame.sprite.Group()
        self.foreground_sprites_2 = pygame.sprite.Group()
    
    def custdraw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        for sprite in sorted(self.foreground_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
        
        for sprite in sorted(self.foreground_sprites_2, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)