import pygame, pytmx, json, sys, pyscroll
from support import *
from tile import *
from world import *
from player import Player
from npc import NPC
from dialog_box import DialogBox

class World:
    def __init__(self, data, new, game):
        self.display_surface = pygame.display.get_surface()
        self.load_save = new
        self.clock = pygame.time.Clock()
        self.data = data
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        pygame.mixer.music.load("./resources/audio/music/Kevin MacLeod - Cipher.mp3")
        pygame.mixer.music.play()
        
        self.loaded = False
        self.game = game
        self.create_map()

        
        with open('./data/dialogs.json', encoding="utf8") as f:
            self.dialog_data = json.load(f)
            
       
        self.dialog_box = DialogBox(self.display_surface, self.data, self.game)

        
        self.dialog_box.set_dialog_data(self.dialog_data)
        
    def load_tileset(self, path, tile_size, scale_factor=3):
        
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
        
      
        map_data = pyscroll.TiledMapData(self.tmx_data)
        map_layer = pyscroll.BufferedRenderer(map_data, self.display_surface.get_size())
        map_layer.zoom = 3


        self.map_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)

        self.obstacle_sprites = pygame.sprite.Group()

        collision_layer = self.tmx_data.get_layer_by_name('collision')
        for x, y, gid in collision_layer:
            if gid != 0:  # gid 0 means no tile
                tile = self.tmx_data.get_tile_image_by_gid(gid)
                if tile:  
                    obstacle = pygame.sprite.Sprite(self.obstacle_sprites)
                    obstacle.rect = pygame.Rect(x * self.tmx_data.tilewidth, 
                                                y * self.tmx_data.tileheight, 
                                                self.tmx_data.tilewidth, 
                                                self.tmx_data.tileheight)

        if self.load_save == True:
            player_position = (self.data['pos_x'], self.data['pos_y'])
        else:
            player_position = (516, 678) 

        # Создаем NPC, x-12, y-34
        self.npc_list = [
            NPC((578,678),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # 0
            NPC((700,590),self.map_group,self.data,"dmitri",'./resources/textures/npc/2/down_idle/1.png'), # 1
            NPC((700,490),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/3/down_idle/1.png'),
            NPC((278,468),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/4/down_idle/1.png'),
            NPC((381,702),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/5/down_idle/1.png'),
            NPC((590,900),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/6/down_idle/1.png'), # 5
            NPC((430,210),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/7/down_idle/1.png'), # all of the above in city
            NPC((420,1600),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/8/down_idle/1.png'), # bottomleft fortress guy
            NPC((1280,230),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/9/down_idle/1.png'), # top village guy
            NPC((1240,607),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/10/down_idle/1.png'), # left of village fountain
            NPC((1764,401),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # 10     shore guy
            NPC((1244,900),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # picnic guy
            NPC((1088,1274),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # midleft village
            NPC((1804,1722),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # bottom right
            NPC((1311,1414),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # waterfall
            NPC((1712,1252),self.map_group,self.data,"tutorial-npc",'./resources/textures/npc/1/down_idle/1.png'), # 15     farmer
        ]
        
        self.player = Player(player_position, self.obstacle_sprites, self.data)
        self.map_group.add(self.player)
        for npc in self.npc_list:
            self.map_group.add(npc)
        
        
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000  
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.QUIT:
                    if self.load_save:
                        with open('./data/savedata.json', 'w') as store_data: 
                            json.dump(self.player.data, store_data, indent=4) 
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.dialog_box.dialog_active:
                    self.dialog_box.advance()
            
            self.display_surface.fill('#1E7CB7')
            self.run_world()
            
            # text_surface = self.font.render(str(self.player.rect.x)+","+str(self.player.rect.y), True, pygame.Color('white'))
            # rect = text_surface.get_rect(topleft=(1,1))
            # self.display_surface.blit(text_surface, rect)
        
            pygame.display.update()

    def run_world(self):
        npcs = [sprite for sprite in self.map_group.sprites() if isinstance(sprite, NPC)]
        if not self.dialog_box.dialog_active:
            self.player.input(npcs) 
        # else:
        #   
        #     keys = pygame.key.get_pressed()
        #     if keys[pygame.K_e]:
        #         self.dialog_box.advance()
        
        self.map_group.center(self.player.rect.center)

        for sprite in self.map_group.sprites():
            if isinstance(sprite, NPC):
                sprite.update(self.player.rect.center) 
            else:
                sprite.update()


        self.map_group.draw(self.display_surface)

       
        # for npc in self.npc_list:
        #     if npc.player_nearby and not self.dialog_box.dialog_active:
        #         if pygame.key.get_pressed()[pygame.K_e]:
        #             self.dialog_box.load_dialog(npc.dialog_id)
        #             self.interact_with_npc(npc.dialog_id)

        
        if self.dialog_box.dialog_active:
            self.dialog_box.render()

        self.loaded = True
        
        
    def interact_with_npc(self, npc_id):
        npc_data = self.data.get('npc_interactions', {}).get(npc_id, {'dialog_seen': False})

        
        if npc_data['dialog_seen']:
           
            self.dialog_box.load_dialog(f"{npc_id}.post")
        else:
            
            self.dialog_box.load_dialog(f"{npc_id}.main")

  
        self.dialog_box.mark_dialog_as_seen(npc_id)

        
    # Пауза
    def pause_screen(self):
        paused = True
        overlay = pygame.Surface(self.display_surface.get_size())
        overlay.set_alpha(128)  
        overlay.fill((50, 50, 50))  
        font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        pygame.mixer.music.pause()

        button_color = pygame.Color('white')
        button_hover_color = pygame.Color('yellow')
    
        buttons = [
        {"text": "Продолжить", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 - 20, 150, 50), "action": "resume"},
        {"text": "В главное меню", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 + 50, 150, 50), "action": "mainmenu"},
        {"text": "Выйти", "rect": pygame.Rect(self.display_surface.get_width() // 2 - 75, self.display_surface.get_height() // 2 + 120, 150, 50), "action": "quit"},
        ]
        
        while paused:
            
            self.display_surface.blit(overlay, (0, 0))
            
            pause_text = titlefont.render("Пауза", True, pygame.Color('white'))
            self.display_surface.blit(pause_text, (self.display_surface.get_width() // 2 - pause_text.get_width() // 2, 128 - pause_text.get_height() // 2))
            
            mouse_pos = pygame.mouse.get_pos()

            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    text_color = button_hover_color
                else:
                    text_color = button_color
                
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
