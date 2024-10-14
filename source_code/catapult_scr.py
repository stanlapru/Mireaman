import pygame, json
from settings import *
from support import *
from tile_platformer import TilePlatformer
from player_platformer import PlayerPlatformer
from npc_platformer import NPCPlatformer
from dialog_box import DialogBox

#Background color
BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

#Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

class CatapultHall:
    def __init__(self, screen, data, game):
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.data = data
        self.game = game
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.done = False
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Empty (52 Kilobytes) SNES Cover [4mat] (256 kbps).mp3")
        pygame.mixer.music.play(-1)
        self.create_map()
        
        # If your dialog data is in a JSON file, you can load it here
        with open('./data/dialogs.json', encoding="utf8") as f:
            self.dialog_data = json.load(f)
            
        # Initialize the dialog box
        self.dialog_box = DialogBox(self.display_surface, self.data, self.game)

        # Pass dialog data to dialog box
        self.dialog_box.set_dialog_data(self.dialog_data)
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./resources/tmx/hall2/hall2_collision_broken.csv'),
            'boundary': import_csv_layout('./resources/tmx/hall2/hall2_collision.csv'),
            'decorations': import_csv_layout('./resources/tmx/hall2/hall2_decorations.csv'),
            'decorations2': import_csv_layout('./resources/tmx/hall2/hall2_decorations2.csv'),
            'solids': import_csv_layout('./resources/tmx/hall2/hall2_background.csv'),
            'solids': import_csv_layout('./resources/tmx/hall2/hall2_background_broken.csv'),
            'wall': import_csv_layout('./resources/tmx/hall2/hall2_wall.csv'),
            'wall': import_csv_layout('./resources/tmx/hall2/hall2_wall_broken.csv'),
        }
        graphics = {
            # 'overworld': import_folder('./resources/tmx/platformer/Assets/')
            'Room_Builder_free_16x16': import_folder("./resources/tmx/tsx/16x16/Room_Builder_free_16x16.png")
        }

        self.interactable_objects = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.boundary_tiles = pygame.sprite.Group()

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
                        if style == 'boundary2':
                            TilePlatformer((x,y), [self.obstacle_sprites, self.boundary_tiles], 'tile_surface')
                        # if style == 'decorations1' or style == 'decorations2' or style == 'decorations3':
                        #     Tile((x,y), [self.visible_sprites], 'walkable')
                        # if style == 'solids1' or style == 'solids2':
                        #     Tile((x,y), [self.visible_sprites], 'solid')
        #         if col == 'x':
        #             Tile((x,y),[self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':

        self.npc_list = [
            NPCPlatformer((1500,1825),[self.visible_sprites],self.obstacle_sprites,'./resources/textures/npc/1/down_idle/1.png', 'tutorial-npc'),
            NPCPlatformer((1600,1825),[self.visible_sprites],self.obstacle_sprites,'./resources/textures/npc/9/down_idle/1.png', 'rector')
        ]
        
        self.player = PlayerPlatformer((1200,1800),[self.visible_sprites], self.obstacle_sprites)
        
        self.characters.add(self.player)
        for npc in self.npc_list:
            self.characters.add(npc)
    
    def run(self):
        self.screen.fill((32,23,41))
        self.visible_sprites.custom_draw(self.player)
         # Update all sprites
        for sprite in self.visible_sprites.sprites():
            if isinstance(sprite, NPCPlatformer):
                sprite.update(self.player.rect.center)  # Pass player's position to NPC
            elif isinstance(sprite, PlayerPlatformer):
                sprite.update(self.npc_list)
            else:
                sprite.update()
        
        # if not self.dialog_box.dialog_active:
        #     self.player.input(self.npc_list)
        
        # Check if player is interacting with any NPC
        for npc in self.npc_list:
            if npc.player_nearby and not self.dialog_box.dialog_active:
                if pygame.key.get_pressed()[pygame.K_e]:
                    self.dialog_box.load_dialog(npc.dialog_id, "main")
                    self.interact_with_npc(npc.dialog_id)

        # Handle any additional drawing, such as the dialog box
        if self.dialog_box.dialog_active:
            self.dialog_box.render()
            
        if pygame.sprite.spritecollide(self.player, self.boundary_tiles, False):
            self.done = True
            
    def interact_with_npc(self, npc_id):
        """Check dialog state and trigger the appropriate dialog."""
        npc_data = self.data.get('npc_interactions', {}).get(npc_id, {'dialog_seen': False})

        # Check if the main dialog has been seen
        if npc_data['dialog_seen']:
            # Load an alternate dialog (e.g., a second phase or small talk)
            self.dialog_box.load_dialog(f"{npc_id}", "main")
        else:
            # Load the initial dialog
            self.dialog_box.load_dialog(f"{npc_id}","main")

        # Once dialog finishes, mark it as seen
        self.dialog_box.mark_dialog_as_seen(npc_id)

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
        
class YSortCamGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.transform.scale_by(pygame.image.load("./resources/tmx/tsx/hall2.png"),3)
        #self.scale_background(3)
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))

    def scale_background(self, scale_factor):
        width1, height1 = self.floor_surface.get_size()
        new_size1 = (int(width1 * scale_factor), int(height1 * scale_factor))
        self.floor_surface = pygame.transform.scale(self.floor_surface, new_size1)
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
        
