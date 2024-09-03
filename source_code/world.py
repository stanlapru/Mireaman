import pygame, pytmx, json, sys
from support import *
from tile import *
from world import *
from player import Player
from npc import NPC
from dialog_box import DialogBox
from animated_tile import AnimatedTile

class World:
    def __init__(self, data, new):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.obstacle_sprites = YSortCamGroup()
        self.foreground_sprites = ForegroundGroup()
        self.foreground_sprites_2 = ForegroundGroup()
        self.load_save = new
        self.clock = pygame.time.Clock()
        
        self.data = data
        pygame.mixer.music.load("./resources/audio/music/Kevin MacLeod - Cipher.mp3")
        pygame.mixer.music.play()
        self.create_map()
        self.loaded = False

        self.dialog1 = DialogBox(self.display_surface, ['Привет, мне очень нужна помощь с компьютером!', "Он как-то сбоит и просит перевести числа в двоичную систему счисления...", "И ты мне с этим поможешь, потому что выбор для отказа ещё не добавлен в игру. :)"])
        
    def load_tileset(self, path, tile_size, scale_factor=3):
        # This function is defined as above
        tileset_image = pygame.image.load(path).convert_alpha()
        tileset_width, tileset_height = tileset_image.get_size()
        tiles_per_row = tileset_width // tile_size[0]
        tiles_per_col = tileset_height // tile_size[1]
        tiles = []
        
        for row in range(tiles_per_col):
            for col in range(tiles_per_row):
                rect = pygame.Rect(col * tile_size[0], row * tile_size[1], tile_size[0], tile_size[1])
                tile_image = tileset_image.subsurface(rect)
                scaled_tile_image = pygame.transform.scale(tile_image, 
                                        (tile_size[0] * scale_factor, tile_size[1] * scale_factor))
                tiles.append(scaled_tile_image)
        
        return tiles
        
    def create_map(self):
        self.tmx_data = pytmx.util_pygame.load_pygame('./resources/tmx/tsx/map.tmx')
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    try:
                        tile = pygame.transform.scale_by(self.tmx_data.get_tile_image_by_gid(gid),3)
                    except:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        position = (x * TILESIZE, y * TILESIZE)
                        if gid in self.tmx_data.tile_properties:
                            props = self.tmx_data.tile_properties[gid]
                            if 'animation' in props:
                                frames = props['animation']
                                tile_surface = AnimatedTile(position, [self.visible_sprites], frames)
                            else:
                                tile_surface = Tile(position, [self.visible_sprites], tile)
                        else:
                            tile_surface = Tile(position, [self.visible_sprites], tile)
        if self.load_save == True:
            self.player = Player((self.data['pos_x'],self.data['pos_y']),[self.visible_sprites], self.obstacle_sprites, self.data)
        else:
            self.player = Player(
            (1200, 1300),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.data
        )
        
    def run(self):
        running = True
        dt = self.clock.tick(60) / 1000
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.QUIT:
                    if self.new:
                        with open('./data/savedata.json', 'w') as store_data: 
                            json.dump(self.player.data, store_data) 
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.player.dialog_active:  # Advance dialog
                    self.dialog1.advance()
            # if player.interacting and not player.dialog_active:
            #     if 750 < player.rect.x < 850 and 750 < player.rect.y < 850:  # Check proximity to NPC
            #         player.dialog_active = True
            #         self.dialog1.started = True
            #         self.dialog1.finished = False
            #         self.dialog1.current_line = 0  # Reset dialog
            #         self.dialog1.next_line()
            
            # if not self.dialog1.finished:
            #     self.dialog1.display()
            
            # if self.dialog1.finished and self.dialog1.started:
            #     self.dialog1.current_line = 0
            #     player.dialog_active = False
            #     self.ict1()  # Assuming `ict1` is another method in `World`
            self.display_surface.fill('#1E7CB7')
            self.run_world()  # Call the method that updates and draws the world
            pygame.display.update()
            self.clock.tick(60)  # Ensure the game runs at the correct FPS

    def run_world(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player, self.foreground_sprites, self.foreground_sprites_2)
        

        
        self.loaded = True
        
    # Пауза
    def pause_screen(self):
        paused = True
        overlay = pygame.Surface(self.display_surface.get_size())
        overlay.set_alpha(128)  # Set transparency (128 out of 255)
        overlay.fill((50, 50, 50))  # Dark grey overlay
        font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        pygame.mixer.music.pause()

        button_color = pygame.Color('white')
        button_hover_color = pygame.Color('yellow')
    
        buttons = [
        {"text": "Продолжить", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 - 20, 150, 50), "action": "resume"},
        {"text": "Настройки", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 + 50, 150, 50), "action": "options"},
        {"text": "В главное меню", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 + 120, 150, 50), "action": "mainmenu"},
        {"text": "Выйти", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 + 190, 150, 50), "action": "quit"},
        ]
        
        while paused:
            
            self.display_surface.blit(overlay, (0, 0))
            
            pause_text = titlefont.render("Пауза", True, pygame.Color('white'))
            self.display_surface.blit(pause_text, (self.display_surface.get_width() // 2 - pause_text.get_width() // 2, 128 - pause_text.get_height() // 2))
            
            mouse_pos = pygame.mouse.get_pos()

            for button in buttons:
                # Change text color on hover
                if button["rect"].collidepoint(mouse_pos):
                    text_color = button_hover_color
                else:
                    text_color = button_color
                
                # Render the button text without background
                button_text = font.render(button["text"], True, text_color)
                self.display_surface.blit(button_text, (button["rect"].x + button["rect"].width // 2 - button_text.get_width() // 2, button["rect"].y + button["rect"].height // 2 - button_text.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        pygame.mixer.music.unpause()
                        paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["action"] == "resume":
                                pygame.mixer.music.unpause()
                                paused = False
                            elif button["action"] == "options":
                                print('options')
                            elif button["action"] == "mainmenu":
                                paused = False
                                self.menu_screen()
                            elif button["action"] == "quit":
                                pygame.quit()
                                sys.exit()
                    
            pygame.display.flip()
            #self.clock.tick(10)  # Slow down the loop for the pause screen
        
class YSortCamGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.floor_surface = pygame.image.load("./resources/textures/environment/world_big.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        
    def custom_draw(self, player, foreground_sprites, foreground_sprites_2):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #floor_offset_pos = self.floor_rect.topleft - self.offset
        #self.display.blit(self.floor_surface, floor_offset_pos)
        
        # Объединяем все спрайты для сортировки и отрисовки
        all_sprites = sorted(
            self.sprites() + foreground_sprites.sprites() + foreground_sprites_2.sprites(),
            key=lambda sprite: sprite.rect.centery
        )
        
        for sprite in all_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)


class ForegroundGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        self.foreground_sprites = pygame.sprite.Group()
        self.foreground_sprites_2 = pygame.sprite.Group()
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        for sprite in sorted(self.foreground_sprites, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
        
        for sprite in sorted(self.foreground_sprites_2, key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)