import pygame, pytmx, json, sys, pyscroll
from support import *
from tile import *
from world import *
from player import Player
from npc import NPC
from dialog_box import DialogBox

class World:
    def __init__(self, data, new):
        self.display_surface = pygame.display.get_surface()
        self.load_save = new
        self.clock = pygame.time.Clock()
        self.data = data
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        pygame.mixer.music.load("./resources/audio/music/Kevin MacLeod - Cipher.mp3")
        pygame.mixer.music.play()
        self.create_map()
        self.loaded = False
        
        self.npc_list = [
            NPC((250,250),self.map_group,self.data,"tutorial_npc")
        ]
        
        # Initialize the dialog box
        self.dialog_box = DialogBox(self.display_surface)

        # If your dialog data is in a JSON file, you can load it here
        with open('./data/dialogs.json', encoding="utf8") as f:
            self.dialog_data = json.load(f)

        # Pass dialog data to dialog box
        self.dialog_box.set_dialog_data(self.dialog_data)
        
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
        # Load the Tiled map
        self.tmx_data = pytmx.util_pygame.load_pygame('./resources/tmx/tsx/map.tmx')
        
        # Create the map data and renderer
        map_data = pyscroll.TiledMapData(self.tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.display_surface.get_size())
        map_layer.zoom = 3

        # Create the Pyscroll group
        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)

        self.obstacle_sprites = pygame.sprite.Group()

        collision_layer = self.tmx_data.get_layer_by_name('collision')
        for x, y, gid in collision_layer:
            if gid != 0:  # gid 0 means no tile
                tile = self.tmx_data.get_tile_image_by_gid(gid)
                if tile:  # If there's a tile (i.e., a filled tile, not empty)
                    obstacle = pygame.sprite.Sprite(self.obstacle_sprites)
                    obstacle.rect = pygame.Rect(x * self.tmx_data.tilewidth, 
                                                y * self.tmx_data.tileheight, 
                                                self.tmx_data.tilewidth, 
                                                self.tmx_data.tileheight)

        # Initialize player position
        if self.load_save == True:
            player_position = (self.data['pos_x'], self.data['pos_y'])
        else:
            player_position = (1200, 1300)  # Default player start position

        # Create player sprite and add to map group
        self.player = Player(player_position, self.obstacle_sprites, self.data)
        self.map_group.add(self.player)
        self.npc = NPC((250,250),self.map_group,self.data,"intro")
        self.map_group.add(self.npc)
        
        
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000  # Delta time for smooth movement
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.QUIT:
                    if self.load_save:
                        with open('./data/savedata.json', 'w') as store_data: 
                            json.dump(self.player.data, store_data) 
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.dialog_box.dialog_active: # Advance dialog
                    print('advancing')
                    self.dialog_box.advance()
            
            self.display_surface.fill('#1E7CB7')
            self.run_world()
            npcs = [sprite for sprite in self.map_group.sprites() if isinstance(sprite, NPC)]
            self.player.input(npcs)
            pygame.display.update()

    def run_world(self):
        self.map_group.center(self.player.rect.center)

        # Update all sprites
        for sprite in self.map_group.sprites():
            if isinstance(sprite, NPC):
                sprite.update(self.player.rect.center)  # Pass player's position to NPC
            else:
                sprite.update()

        # Draw the map and sprites
        self.map_group.draw(self.display_surface)

        # Check if player is interacting with any NPC
        for npc in self.npc_list:
            if npc.player_nearby and not self.dialog_box.dialog_active:
                if pygame.key.get_pressed()[pygame.K_e]:
                    self.dialog_box.load_dialog(npc.dialog_id)

        # Handle any additional drawing, such as the dialog box
        if self.dialog_box.dialog_active:
            self.dialog_box.render()

        self.loaded = True
        # pygame.display.update()
        
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
                                from main import Game
                                self.game = Game()
                                self.game.menu_screen()
                            elif button["action"] == "quit":
                                pygame.quit()
                                sys.exit()
                    
            pygame.display.flip()
            #self.clock.tick(10)  # Slow down the loop for the pause screen
