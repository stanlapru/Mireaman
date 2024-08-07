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
        self.platformer_world = PlatformerWorld()
        
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
                if event.type == pygame.MOUSEMOTION:
                    if main_screen:
                        main_screen.handle_mouse_motion(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # atrocious code here, move on
                    if main_screen.buttons[0].is_clicked(event.pos):
                        running = False
                        self.run(False)
                    if main_screen.buttons[1].is_clicked(event.pos):
                        running = False
                        self.run(True)
                    if main_screen.buttons[3].is_clicked(event.pos):
                        running = False
                        self.credits_screen()
                    main_screen.handle_mouse_click(event.pos)
            main_screen.draw()
            pygame.display.flip()
            
    def platformer_screen(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            self.screen.fill('#1E7CB7')
            self.platformer_world.run()
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
                if event.type == pygame.QUIT:
                    if new == True:
                        with open('./data/savedata.json', 'w') as store_data: 
                            json.dump(world_screen.player.data, store_data) 
                    running = False
                    pygame.quit()
                    sys.exit()
            self.screen.fill('#1E7CB7')
            world_screen.run()
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