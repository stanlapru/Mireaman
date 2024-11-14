# LAUNCH THIS
import pygame
import sys
import json, random, string
from settings import *
from world import World
from start_screen import StartScreen
from credits_screen import CreditsScreen
from error_screen import ErrorScreen
from platformer_screen import PlatformerWorld
from tutorial_hall import TutorialHall
from binary_scr import BinaryHall
from catapult_scr import CatapultHall
from transition_screen import PortalScreen
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
            'npc_interactions': {},
            'sound_on': False,
        }
        
        try: 
            with open('./data/savedata.json') as load_file: 
                self.savedata = json.load(load_file) 
                self.scr_width = load_file.read()
        except: 
            print('No savefile found. Creating new one.')
            with open('./data/savedata.json', 'w') as store_file: 
                json.dump(self.savedata, store_file, indent=4) 
        
        pygame.init()
        pygame.mixer.init()
        # display_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.savedata.get('width', 1280), (self.savedata.get('height', 720))))
        pygame.display.set_caption("Мир грифонов")
        
        cursor_surface = pygame.image.load('./resources/textures/cursor/Tiles/tile_0049.png')
        cursor_surface_32x32 = pygame.transform.scale(cursor_surface, (32, 32))
        hotspot = (0, 0)
        cursor = pygame.cursors.Cursor(hotspot, cursor_surface_32x32)
        pygame.mouse.set_cursor(cursor)
        
        self.clock = pygame.time.Clock()
        
        self.current_screen = None
        self.screens = {}
        
        self.menu_screen()

    def set_resolution(self):
        pygame.display.set_mode((self.savedata.get('width', 1280), (self.savedata.get('height', 720))))

    # Пауза
    def pause_screen(self):
        paused = True
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128) 
        overlay.fill((50, 50, 50)) 
        font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        pygame.mixer.music.pause()

        button_color = pygame.Color('white')
        button_hover_color = pygame.Color('yellow')
    
        buttons = [
        {"text": "Продолжить", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 - 20, 150, 50), "action": "resume"},
        {"text": "В главное меню", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 50, 150, 50), "action": "mainmenu"},
        {"text": "Выйти", "rect": pygame.Rect(self.screen.get_width() // 2 - 75, self.screen.get_height() // 2 + 120, 150, 50), "action": "quit"},
        ]
        
        while paused:
            
            self.screen.blit(overlay, (0, 0))
            
            pause_text = titlefont.render("Пауза", True, pygame.Color('white'))
            self.screen.blit(pause_text, (self.screen.get_width() // 2 - pause_text.get_width() // 2, 128 - pause_text.get_height() // 2))
            
            mouse_pos = pygame.mouse.get_pos()

            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    text_color = button_hover_color
                else:
                    text_color = button_color
                
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

    # Главное меню
    def menu_screen(self):
        running = True
        main_screen = StartScreen(self.screen, self)
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
                    # if main_screen.buttons[0].is_clicked(event.pos):
                    #     running = False
                    #     self.run(False) # new
                    if not main_screen.show_resolution and not main_screen.show_settings:
                        if main_screen.control_button.is_clicked(event.pos):
                            running = False
                            self.platformer_screen()
                        if main_screen.buttons[1].is_clicked(event.pos): 
                            running = False
                            with open('./data/savedata.json', 'r') as file:
                                data = json.load(file)
                            if data.get('current_screen') == 'tutorial_hall':
                                self.tutorial_hall()
                            if data.get('current_screen') == 'catapult_hall':
                                self.catapult_hall()
                            if data.get('current_screen') == 'binary_hall':
                                self.binary_hall()
                        if main_screen.buttons[3].is_clicked(event.pos): # credits
                            running = False
                            self.credits_screen()
                    main_screen.handle_mouse_click(event.pos)
            main_screen.draw()
            pygame.display.flip()
            
    # Экран платформера
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
            self.screen.fill('#40A3FF')
            platformer_world.run()
            platformer_world.check_interactable_hover()
            pygame.display.update()
            self.clock.tick(FPS)

    # Экран с порталом после выбора предметов
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
                self.tutorial_hall()
            portal_scr.run()
            pygame.display.update()
            self.clock.tick(FPS)
    
    def tutorial_hall(self):
        tutorial_scr = TutorialHall(self.screen, self.savedata, self)
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
                if event.type == pygame.MOUSEBUTTONDOWN and tutorial_scr.dialog_box.dialog_active: 
                    tutorial_scr.dialog_box.advance()
                
            if tutorial_scr.done == True:
                self.savedata['current_screen'] = 'catapult_hall'
                with open('./data/savedata.json', 'w') as store_file: 
                    json.dump(self.savedata, store_file, indent=4) 
                self.catapult_hall()
            tutorial_scr.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def catapult_hall(self):
        catapult_scr = CatapultHall(self.screen, self.savedata, self)
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
                if event.type == pygame.MOUSEBUTTONDOWN and catapult_scr.dialog_box.dialog_active:
                    catapult_scr.dialog_box.advance()
                catapult_scr.task_overlay.handle_event(event)
            if catapult_scr.done == True:
                self.savedata['current_screen'] = 'binary_hall'
                with open('./data/savedata.json', 'w') as store_file: 
                    json.dump(self.savedata, store_file, indent=4) 
                self.binary_hall()
            catapult_scr.run()
            pygame.display.update()
            self.clock.tick(FPS)
            
    def binary_hall(self):
        binary_scr = BinaryHall(self.screen, self.savedata, self)
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
                if event.type == pygame.MOUSEBUTTONDOWN and binary_scr.dialog_box.dialog_active: 
                    binary_scr.dialog_box.advance()
                binary_scr.task_overlay.handle_event(event)
            if binary_scr.done == True:
               
                self.run(False)
            binary_scr.run()
            pygame.display.update()
            self.clock.tick(FPS)
    
    # Титры
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
    
    # Экран с миром
    def run(self, new):
        world = World(self.savedata, new, self)
        world.run()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
                    self.menu_screen()
            error_screen.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
    def switch_screen(self, screen_name):
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]
        else:
            game.error('Call to nonexistent screen.')
            
            
if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except Exception as e:
        if hasattr(e,'message'):
            game.error(e.message)
        else:
            game.error(e)