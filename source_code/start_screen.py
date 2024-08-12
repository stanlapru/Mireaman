import pygame
import sys
from menu_button import MenuButton
from settings import *

class StartScreen:
    def __init__(self, game: pygame.Surface):
        self.game = game
        pygame.font.init()
        self.titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.smallfont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 12)
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Stasis.mp3")
        pygame.mixer.music.play(-1)

        self.bg_image1 = pygame.image.load('./resources/textures/mainmenu/bg_layer.png')
        self.bg_image2 = pygame.image.load('./resources/textures/mainmenu/bg_layer2.png')
        self.bg_scroll1 = 0
        self.bg_scroll2 = 0

        self.scale_background(2.0, 1)

        self.buttons = []
        self.settings_buttons = []
        self.create_buttons()
        self.show_settings = False
        
    def create_buttons(self):
        self.buttons = [
            MenuButton('Новая игра', (self.game.get_width() // 2, 300), self.font, self.new_game),
            MenuButton('Загрузить игру', (self.game.get_width() // 2, 375), self.font, self.load_game),
            MenuButton('Настройки', (self.game.get_width() // 2, 450), self.font, self.show_settings_menu),
            MenuButton('Титры', (self.game.get_width() // 2, 525), self.font, self.credits),
            MenuButton('Выход', (self.game.get_width() // 2, 600), self.font, self.quit_game)
        ]
        self.settings_buttons = [
            MenuButton('Звук', (self.game.get_width() // 2, 150), self.font, self.adjust_volume),
            MenuButton('Назад', (self.game.get_width() // 2, 200), self.font, self.hide_settings_menu)
        ]

    def new_game(self):
        pygame.mixer.music.stop()
        print("Новая игра")

    def load_game(self):
        print("Загрузить игру")

    def show_settings_menu(self):
        self.show_settings = True

    def hide_settings_menu(self):
        self.show_settings = False

    def credits(self):
        print("Титры")
        pygame.mixer.music.stop()
        
    def quit_game(self):
        pygame.quit()
        sys.exit()

    def adjust_volume(self):
        print("Изменение громкости")
    
    def handle_mouse_click(self, pos: tuple[int, int]):
        for button in (self.settings_buttons if self.show_settings else self.buttons):
            if button.is_clicked(pos):
                button.on_click()
                break

    def handle_mouse_motion(self, pos):
        for button in (self.settings_buttons if self.show_settings else self.buttons):
            button.on_hover(button.is_clicked(pos))
    
    def draw(self):
        self.game.fill((128, 128, 255))
        
        self.scroll_background()

        for button in (self.settings_buttons if self.show_settings else self.buttons):
            button.draw(self.game)

        #self.render_text("indev v0.0.0", (0,0))
        self.render_title_text("Мир грифонов", (self.game.get_width() // 2, 100))

    def render_title_text(self, text, position):
        text_surface = self.titlefont.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=position) 
        self.game.blit(text_surface, text_rect)

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))  
        text_rect = text_surface.get_rect(center=position)  
        self.game.blit(text_surface, text_rect) 
        
    def render_text(self, text, position):
        text_surface = self.smallfont.render(text, True, (255, 255, 255))  
        text_rect = text_surface.get_rect(topleft=position)  
        self.game.blit(text_surface, text_rect) 
        
    def scale_background(self, scale_factor, scale_factor2):
        width1, height1 = self.bg_image1.get_size()
        width2, height2 = self.bg_image2.get_size()

        new_size1 = (int(width1 * scale_factor), int(height1 * scale_factor))
        new_size2 = (int(width2 * scale_factor2), int(height2 * scale_factor2))

        self.bg_image1 = pygame.transform.scale(self.bg_image1, new_size1)
        self.bg_image2 = pygame.transform.scale(self.bg_image2, new_size2)

    def scroll_background(self):
        self.bg_scroll1 -= 0.1
        self.bg_scroll2 -= 0.02

        if self.bg_scroll1 <= -self.bg_image1.get_width():
            self.bg_scroll1 = 0
        if self.bg_scroll2 <= -self.bg_image2.get_width():
            self.bg_scroll2 = 0

        self.game.blit(self.bg_image2, (self.bg_scroll2, self.game.get_height() - self.bg_image2.get_height() - 160))
        self.game.blit(self.bg_image2, (self.bg_scroll2 + self.bg_image2.get_width(), self.game.get_height() - self.bg_image2.get_height() - 160))

        self.game.blit(self.bg_image1, (self.bg_scroll1, self.game.get_height() - self.bg_image1.get_height()))
        self.game.blit(self.bg_image1, (self.bg_scroll1 + self.bg_image1.get_width(), self.game.get_height() - self.bg_image1.get_height()))