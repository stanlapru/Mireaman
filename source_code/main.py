# LAUNCH THIS
import pygame
import pygame_gui
import subprocess
import threading
import sys
import threading
import json
from settings import *
from world import *
from start_screen import *
from credits_screen import *
from error_screen import *
from platformer_screen import *
from loading_screen import *
from transition_screen import *
from problems.ict.ict1 import ICTone

class Game:
    def __init__(self):
        
        self.savedata = {
            'pos_x': 1200,
            'pos_y': 1300,
            'subjects': [],
            'fps': 60,
            'demo_mode': False,
            'width': 1280,
            'height': 720,
        }
        
        try: 
            # the file already exists 
            with open('./data/savedata.json') as load_file: 
                self.savedata = json.load(load_file) 
        except: 
            # create the file and store initial values 
            with open('./data/savedata.json', 'w') as store_file: 
                json.dump(self.savedata, store_file) 
        
        pygame.init()
        pygame.mixer.init()
        display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мир грифонов")
        
        # Custom cursor
        cursor_surface = pygame.image.load('./resources/textures/cursor/Tiles/tile_0049.png')
        cursor_surface_32x32 = pygame.transform.scale(cursor_surface, (32, 32))
        hotspot = (0, 0)
        cursor = pygame.cursors.Cursor(hotspot, cursor_surface_32x32)
        pygame.mouse.set_cursor(cursor)
        
        self.clock = pygame.time.Clock()
        # self.world = World()
        
        self.current_screen = None
        self.screens = {}
        # self.initialize_screens()
        
        self.menu_screen()
        
    def initialize_screens(self):
        self.screens['start'] = StartScreen(self)
        self.screens['credits'] = CreditsScreen(self)
        self.screens['world'] = World(self)
        self.screens['platformer'] = PlatformerWorld(self)
        self.screens['error'] = ErrorScreen(self)
        self.screens['loading'] = LoadingScreen(self)

        self.switch_screen('start')

    def pause_screen(self):
        paused = True
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)  # Set transparency (128 out of 255)
        overlay.fill((50, 50, 50))  # Dark grey overlay
        font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        pygame.mixer.music.pause()

        button_color = pygame.Color('white')
        button_hover_color = pygame.Color('yellow')
    
        buttons = [
        {"text": "Продолжить", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 - 20, 150, 50), "action": "resume"},
        {"text": "Настройки", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 50, 150, 50), "action": "options"},
        {"text": "В главное меню", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 120, 150, 50), "action": "mainmenu"},
        {"text": "Выйти", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 190, 150, 50), "action": "quit"},
        ]
        
        while paused:
            
            self.screen.blit(overlay, (0, 0))
            
            pause_text = titlefont.render("Пауза", True, pygame.Color('white'))
            self.screen.blit(pause_text, (self.screen.get_width() // 2 - pause_text.get_width() // 2, 128 - pause_text.get_height() // 2))
            
            mouse_pos = pygame.mouse.get_pos()

            for button in buttons:
                # Change text color on hover
                if button["rect"].collidepoint(mouse_pos):
                    text_color = button_hover_color
                else:
                    text_color = button_color
                
                # Render the button text without background
                button_text = font.render(button["text"], True, text_color)
                self.screen.blit(button_text, (button["rect"].x + button["rect"].width // 2 - button_text.get_width() // 2, button["rect"].y + button["rect"].height // 2 - button_text.get_height() // 2))

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

        
    def menu_screen(self):
        running = True
        main_screen = StartScreen(self.screen)
        while running:
            self.screen.fill(pygame.Color('#d87093'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if main_screen:
                        main_screen.handle_mouse_motion(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # atrocious code here, move on
                    # if main_screen.buttons[0].is_clicked(event.pos):
                    #     running = False
                    #     self.run(False) # new
                    if main_screen.buttons[0].is_clicked(event.pos): # new game; platformer selection
                        running = False
                        self.platformer_screen()
                    if main_screen.buttons[1].is_clicked(event.pos): # load existing game
                        running = False
                        self.run(True) # load
                    if main_screen.buttons[3].is_clicked(event.pos): # credits
                        running = False
                        self.credits_screen()
                    main_screen.handle_mouse_click(event.pos)
            main_screen.draw()
            pygame.display.flip()
            
    def platformer_screen(self):
        platformer_world = PlatformerWorld(self.screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            if platformer_world.portal.touched == True:
                platformer_world.portal.save_selected_subjects()
                self.portal_screen()
            self.screen.fill('#1E7CB7')
            platformer_world.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def portal_screen(self):
        portal_scr = PortalScreen(self.screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            if portal_scr.done == True:
                self.run(False)      
            portal_scr.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def credits_screen(self):
        running = True
        credits_screen = CreditsScreen(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_ESCAPE or event.type == pygame.K_SPACE:
                    running = False
                    self.menu_screen()
            if credits_screen.draw():
                running = False
                self.menu_screen()
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def run(self, new):
        running = True
        world_screen = World(self.savedata, new)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.QUIT:
                    if new == True:
                        with open('./data/savedata.json', 'w') as store_data: 
                            json.dump(world_screen.player.data, store_data) 
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and world_screen.player.dialog_active:  # Advance dialog
                    world_screen.dialog1.advance()
            player = world_screen.player
            if player.interacting and not player.dialog_active:
                if 750 < player.rect.x < 850 and 750 < player.rect.y < 850:  # Check proximity to NPC
                    player.dialog_active = True
                    world_screen.dialog1.started = True
                    world_screen.dialog1.finished = False
                    world_screen.dialog1.current_line = 0  # Reset dialog
                    world_screen.dialog1.next_line()
            
            if world_screen.dialog1.finished == False:
                world_screen.dialog1.display()
            
            if world_screen.dialog1.finished and world_screen.dialog1.started:
                world_screen.dialog1.current_line = 0
                player.dialog_active = False
                self.ict1()
            self.screen.fill('#1E7CB7')
            world_screen.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def ict1(self):
        running = True
        task_screen = ICTone(self.screen)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_screen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 400 <= x <= 400 + 8 * (36 + 10) and 250 <= y <= 250 + 36:
                        selected = (x - 400) // (36 + 10)
                        task_screen.binary_boxes[selected] = 1 if task_screen.binary_boxes[selected] == 0 else 0
                    if 325 <= x <= 325 + 150 and 450 <= y <= 450 + 50:
                        task_screen.check_answer()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            if task_screen.score == 10:
                running = False
                self.run(False)
            self.screen.fill('#000000')
            task_screen.draw()
            pygame.display.update()
            self.clock.tick(FPS)
    
    def error(self, err):
        running = True
        error_screen = ErrorScreen(self.screen, self.clock, err)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            error_screen.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
    def switch_screen(self, screen_name):
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]
            
if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except Exception as e:
        if hasattr(e,'message'):
            game.error(e.message)
        else:
            game.error(e)