import pygame, time, random
from settings import *
from support import *
from tile_platformer import TilePlatformer
from player_platformer import PlayerPlatformer
from interactable import InteractableObject
from portal import Portal

BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

MAP_COLLISION_LAYER = 1

class PlatformerWorld:
    def __init__(self, screen):
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Empty (52 Kilobytes) SNES Cover [4mat] (256 kbps).mp3")
        pygame.mixer.music.play(-1)
        self.create_map()
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./resources/tmx/platformer/platformer_collision.csv'),
            'decorations': import_csv_layout('./resources/tmx/platformer/platformer_decorations.csv'),
            'solids': import_csv_layout('./resources/tmx/platformer/platformer_background.csv'),
        }
        graphics = {
            'overworld': import_folder('./resources/tmx/tsx/Overworld/Overworld.png')
        }

        self.interactable_objects = pygame.sprite.Group()

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

        interacted_image = './resources/textures/blocks/selected.png'
        interactable_data = [
            {'pos': (900, 1700), 'object_id': 'math', 'initial_image': './resources/textures/blocks/math.png', 'interacted_image': interacted_image, 'object_id_rus': 'Математика'},
            {'pos': (1100, 1700), 'object_id': 'english', 'initial_image': './resources/textures/blocks/english.png', 'interacted_image': interacted_image, 'object_id_rus': 'Иностранный язык'},
            {'pos': (1300, 1700), 'object_id': 'physics', 'initial_image': './resources/textures/blocks/physics.png', 'interacted_image': interacted_image, 'object_id_rus': 'Физика'},
            {'pos': (1500, 1700), 'object_id': 'coding', 'initial_image': './resources/textures/blocks/coding.png', 'interacted_image': interacted_image, 'object_id_rus': 'Программирование'},
            {'pos': (2100, 1700), 'object_id': 'geography', 'initial_image': './resources/textures/blocks/geography.png', 'interacted_image': interacted_image, 'object_id_rus': 'География'},
            {'pos': (2300, 1700), 'object_id': 'literature', 'initial_image': './resources/textures/blocks/literature.png', 'interacted_image': interacted_image, 'object_id_rus': 'Литература'},
            {'pos': (2500, 1700), 'object_id': 'russian', 'initial_image': './resources/textures/blocks/russian.png', 'interacted_image': interacted_image, 'object_id_rus': 'Русский язык'},
            {'pos': (2700, 1700), 'object_id': 'social', 'initial_image': './resources/textures/blocks/social.png', 'interacted_image': interacted_image, 'object_id_rus': 'Правоведение'},
            {'pos': (3500, 1700), 'object_id': 'chemistry', 'initial_image': './resources/textures/blocks/chemistry.png', 'interacted_image': interacted_image, 'object_id_rus': 'Химия'},
            {'pos': (3700, 1700), 'object_id': 'biology', 'initial_image': './resources/textures/blocks/biology.png', 'interacted_image': interacted_image, 'object_id_rus': 'Биология'},
        ]

        for obj_data in interactable_data:
            g = InteractableObject(obj_data['pos'], [self.visible_sprites], self.obstacle_sprites, object_id=obj_data['object_id'], initial_image=obj_data['initial_image'], interacted_image=obj_data['interacted_image'], obj_id_rus=obj_data['object_id_rus'])
            self.interactable_objects.add(g)
            

        self.player = PlayerPlatformer((1200,1750),[self.visible_sprites], self.obstacle_sprites)
        self.portal = Portal((4800, 1700), [self.visible_sprites, self.obstacle_sprites], self.player)
    
    def run(self):
        self.check_interactable_hover()
        self.visible_sprites.custom_draw(self.player)
        for sprite in self.visible_sprites:
            if isinstance(sprite, PlayerPlatformer):
                sprite.update([], False)
            else:
                sprite.update()
        self.visible_sprites.update_clouds()
        self.draw()
        

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        # self.render_text(str(self.world_mouse_pos), (8,50))
        self.render_text("Выбраны:", (8, 8))
        box_start_x = 200
        box_start_y = 8
        box_size = 48
        spacing = 8
        for object_id in self.player.selected_objects:
            image_path = f'./resources/textures/blocks/{object_id}.png'
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (box_size, box_size))
            position = (box_start_x, box_start_y)
            self.screen.blit(image, position)
            box_start_x += box_size + spacing
        
    def check_interactable_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        world_mouse_x = mouse_pos[0] + self.visible_sprites.offset.x
        world_mouse_y = mouse_pos[1] + self.visible_sprites.offset.y
        self.world_mouse_pos = (int(world_mouse_x), int(world_mouse_y))
        for interactable_object in self.interactable_objects:
            if interactable_object.rect.collidepoint(self.world_mouse_pos):
                self.render_text(interactable_object.obj_id_rus, (mouse_pos[0] + 30, mouse_pos[1] - 30))
        
class YSortCamGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.transform.scale_by(pygame.image.load("./resources/tmx/platformer/platformer2.png"),3)
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        self.clouds = pygame.sprite.Group()
        self.last_cloud_spawn_time = time.time()
        
    def spawn_cloud(self):
        cloud_image_path = random.choice(["./resources/textures/cloud.png", "./resources/textures/cloud2.png"])
        cloud_y = random.randint(50, self.half_height // 2)  
        cloud = Cloud(self.display.get_width(), cloud_y, cloud_image_path)
        self.clouds.add(cloud)

    def update_clouds(self):
        if time.time() - self.last_cloud_spawn_time > 5:
            self.spawn_cloud()
            self.last_cloud_spawn_time = time.time()

        self.clouds.update()
        for cloud in self.clouds:
            if cloud.rect.right < 0:
                cloud.kill() 

    def scale_background(self, scale_factor):
        width1, height1 = self.floor_surface.get_size()
        new_size1 = (int(width1 * scale_factor), int(height1 * scale_factor))
        self.floor_surface = pygame.transform.scale(self.floor_surface, new_size1)
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        
        for cloud in self.clouds:
            self.display.blit(cloud.image, cloud.rect)
            
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
            

            
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 1.5)  # Scale cloud if necessary
        self.rect = self.image.get_rect(midleft=(x, y))
        self.speed = 1  # Cloud movement speed

    def update(self):
        # Move cloud leftward
        self.rect.x -= self.speed
        
