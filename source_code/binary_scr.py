import pygame, json
from settings import *
from support import *
from tile_platformer import TilePlatformer
from player_platformer import PlayerPlatformer
from npc_platformer import NPCPlatformer
from dialog_box import DialogBox

BACKGROUND = (20, 20, 20)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

MAP_COLLISION_LAYER = 1

class BinaryHall:
    def __init__(self, screen, data, game):
        self.screen = screen
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCamGroup()
        self.initial_tiles = pygame.sprite.Group()
        self.alternative_tiles = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.data = data
        self.game = game
        self.completed = False
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.done = False
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Empty (52 Kilobytes) SNES Cover [4mat] (256 kbps).mp3")
        pygame.mixer.music.play(-1)
        self.create_map()
        
        
        with open('./data/dialogs.json', encoding="utf8") as f:
            self.dialog_data = json.load(f)
            

        self.dialog_box = DialogBox(self.display_surface, self.data, self.game)

        
        self.dialog_box.set_dialog_data(self.dialog_data)
        
        self.task_overlay = TaskOverlay(screen, self.font, "Биту необходимо найти файл курсовой работы, но он не знает, где он находится, так как понимает только двоичную систему. Переведи адрес файла - 164 - в понятный для Бита вид.", "10100100", self.dialog_box)
        
    def create_map(self):
        layouts = {
            'boundary2': import_csv_layout('./resources/tmx/hall3/hall3_next.csv'),
            'boundary': import_csv_layout('./resources/tmx/hall3/hall3_collision.csv'),
            'decorations': import_csv_layout('./resources/tmx/hall3/hall3_decorations.csv'),
            'decorations2': import_csv_layout('./resources/tmx/hall3/hall3_decorations2.csv'),
            'solids': import_csv_layout('./resources/tmx/hall3/hall3_background.csv'),
        }
        graphics = {
            # 'overworld': import_folder('./resources/tmx/platformer/Assets/')
            'Room_Builder_free_16x16': import_folder("./resources/tmx/tsx/16x16/Room_Builder_free_16x16.png")
        }

        self.interactable_objects = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.boundary_tiles = pygame.sprite.Group()

        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col != '-1':
                        x = col_idx * TILESIZE
                        y = row_idx * TILESIZE
                        if style in ['boundary']:
                            
                            tile = TilePlatformer((x, y), [self.obstacle_sprites], 'tile_surface')
                            self.initial_tiles.add(tile)
                        elif style in ['boundary2']:
                            
                            tile = TilePlatformer((x, y), [self.obstacle_sprites, self.boundary_tiles], 'tile_surface')
                            # self.alternative_tiles.add(tile)

        self.npc_list = [
            NPCPlatformer((1530,1690),[self.visible_sprites],self.obstacle_sprites,'./resources/textures/npc/12/down_idle/1.png', 'task-2-pre'),
        ]
        # 1200
        self.player = PlayerPlatformer((963,2000),[self.visible_sprites], self.obstacle_sprites)
        
        self.characters.add(self.player)
        for npc in self.npc_list:
            self.characters.add(npc)
    
    def run(self):
        self.screen.fill((32,23,41))
        self.visible_sprites.custom_draw(self.player)
        for sprite in self.visible_sprites.sprites():
            if isinstance(sprite, NPCPlatformer):
                sprite.update(self.player.rect.center) 
            elif isinstance(sprite, PlayerPlatformer):
                sprite.update(self.npc_list, self.task_overlay.show_overlay and not self.task_overlay.is_solved)
            else:
                sprite.update()
        
        
        if not self.task_overlay.show_overlay and self.task_overlay.is_solved and not self.completed:
            self.dialog_box.load_dialog('task-2-pre', "task-2-success")
            self.completed = True
            self.switch_to_alternative_layout()
            
        for npc in self.npc_list:
            if npc.player_nearby and not self.dialog_box.dialog_active and not self.task_overlay.is_solved:
                if pygame.key.get_pressed()[pygame.K_e]:
                    self.dialog_box.load_dialog(npc.dialog_id, "main")
                    self.interact_with_npc(npc.dialog_id)

       
        if self.dialog_box.dialog_active:
            self.dialog_box.render()
            
        if pygame.sprite.spritecollide(self.player, self.boundary_tiles, False):
            self.done = True
            
        
        if self.player.rect.x > 1680:
            self.player.is_task = True
            
        self.task_overlay.update(self.player.rect.x)
        
        self.task_overlay.draw()
        
    def switch_to_alternative_layout(self):
       
        # self.visible_sprites.remove(self.initial_tiles)
        # self.obstacle_sprites.remove(self.initial_tiles)


        self.visible_sprites.add(self.alternative_tiles)
        self.obstacle_sprites.add(self.alternative_tiles)
        
        self.visible_sprites.change_bg()
            
            
    def interact_with_npc(self, npc_id):
        """Check dialog state and trigger the appropriate dialog."""
        npc_data = self.data.get('npc_interactions', {}).get(npc_id, {'dialog_seen': False})

       
        if npc_data['dialog_seen']:
           
            self.dialog_box.load_dialog(f"{npc_id}", "main")
        else:
            
            self.dialog_box.load_dialog(f"{npc_id}","main")

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
        self.floor_surface = pygame.transform.scale_by(pygame.image.load("./resources/tmx/tsx/hall3.png"),3)
        #self.scale_background(3)
        self.floor_rect = self.floor_surface.get_rect(topleft = (0,0))
        
    def change_bg(self):
        self.floor_surface = pygame.transform.scale_by(pygame.image.load("./resources/tmx/tsx/hall3new.png"),3)

    def scale_background(self, scale_factor):
        width1, height1 = self.floor_surface.get_size()
        new_size1 = (int(width1 * scale_factor), int(height1 * scale_factor))
        self.floor_surface = pygame.transform.scale(self.floor_surface, new_size1)
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height*1.5
        
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display.blit(self.floor_surface, floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset_pos)
        
        
class TaskOverlay:
    def __init__(self, screen, font, task_text, correct_answer, dialog_box):
        self.screen = screen
        self.dialog_box = dialog_box
        self.font = font
        self.wrong = False
        self.is_solved = False
        self.task_text = task_text 
        self.correct_answer = correct_answer
        self.input_text = ""  
        self.show_overlay = False  
        self.box_rect = pygame.Rect(0, 0, 400, 1280)  
        self.input_rect = pygame.Rect(400, 720-60, 1280-620, 60)  
        self.enter_button_rect = pygame.Rect(1280-220, 720-60, 220, 60)  

    def draw(self):
        if not self.show_overlay:
            return

        
        pygame.draw.rect(self.screen, (0, 0, 0), self.box_rect)
        self.render_text(self.task_text, (self.box_rect.x + 10, self.box_rect.y + 10), self.box_rect.width - 20)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)
        
        input_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        pygame.draw.rect(self.screen, (0, 255, 0), self.enter_button_rect)
        button_text = self.font.render("Ввод", True, (0, 0, 0))
        self.screen.blit(button_text, (self.enter_button_rect.x + 10, self.enter_button_rect.y + 5))
        
        if self.wrong:
            self.dialog_box.render()
        
        if not self.dialog_box.dialog_active:
            self.wrong = False

    def render_text(self, text, position, wrap_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= wrap_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for idx, line in enumerate(lines):
            line_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surface, (position[0], position[1] + idx * 30))

    def handle_event(self, event):
        if not self.show_overlay:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1] 
            elif event.key == pygame.K_RETURN:
                self.check_answer()
            else:
                self.input_text += event.unicode 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.enter_button_rect.collidepoint(event.pos):
                self.check_answer()

    def check_answer(self):
        if self.input_text.strip().lower() == self.correct_answer.lower():
            print("Correct Answer!")
            self.is_solved = True
        else:
            self.wrong = True
            self.dialog_box.load_dialog('task-2-pre','task-2-fail')
            self.input_text = ""

    def update(self, player_x):
        if player_x >= 1680 and not self.is_solved:
            self.show_overlay = True
        else:
            self.show_overlay = False
