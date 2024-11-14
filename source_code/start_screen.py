import pygame
import sys
import json
from menu_button import MenuButton
from settings import *

class StartScreen:
    def __init__(self, scr: pygame.Surface, game):
        self.scr = scr
        self.game = game
        pygame.font.init()
        self.titlefont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 58)
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.smallfont = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 12)

        self.bg_image1 = pygame.image.load('./resources/textures/mainmenu/bg_layer.png')
        self.bg_image2 = pygame.image.load('./resources/textures/mainmenu/bg_layer2.png')
        self.bg_scroll1 = 0
        self.bg_scroll2 = 0

        self.scale_background(2.0, 1)

        self.controls_shown = False
        self.controls_showing = False
        
        self.buttons = []
        self.settings_buttons = []
        self.show_settings = False
        
        self.sound_on = True
        self.current_resolution = (scr.get_width(), scr.get_height())  
        self.load_settings()
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/Stasis.mp3")
        pygame.mixer.music.play(-1)
        
        if self.save_data.get("sound_on") == False:
            pygame.mixer.music.set_volume(0)
        
        self.create_buttons()
        
    def load_settings(self):
        with open('./data/savedata.json', 'r') as f:
            self.save_data = json.load(f)
        self.sound_on = self.save_data.get("sound_on", True) 
        self.current_resolution = (self.save_data.get("width", (1280)), self.save_data.get("height", (720)))
        
    def save_settings(self):
        self.save_data["sound_on"] = self.sound_on
        self.save_data["width"] = self.current_resolution[0]
        self.save_data["height"] = self.current_resolution[1]
        with open('./data/savedata.json', 'w') as f:
            json.dump(self.save_data, f, indent=4)
        
    def create_buttons(self):
        self.buttons = [
            MenuButton('Новая игра', (self.scr.get_width() // 2, 300), self.font, self.new_game),
            MenuButton('Загрузить игру', (self.scr.get_width() // 2, 375), self.font, self.load_game),
            MenuButton('Настройки', (self.scr.get_width() // 2, 450), self.font, self.show_settings_menu),
            MenuButton('Титры', (self.scr.get_width() // 2, 525), self.font, self.credits),
            MenuButton('Выход', (self.scr.get_width() // 2, 600), self.font, self.quit_game)
        ]
        self.settings_buttons = [
            MenuButton(f'Звук: {"Включен" if self.sound_on else "Выключен"}', (self.scr.get_width() // 2, 375), self.font, self.toggle_sound),
            MenuButton('Разрешение', (self.scr.get_width() // 2, 450), self.font, self.show_resolution_options),
            MenuButton('Назад', (self.scr.get_width() // 2, 525), self.font, self.hide_settings_menu)
        ]

        self.resolution_buttons = [
            MenuButton('1280x720', (self.scr.get_width() // 2, 375), self.font, lambda: self.change_resolution(1280, 720)),
            MenuButton('1920x1080', (self.scr.get_width() // 2, 450), self.font, lambda: self.change_resolution(1920, 1080)),
            MenuButton('Назад', (self.scr.get_width() // 2, 525), self.font, self.hide_resolution_options)
        ]
        
        self.control_button = MenuButton('Нажми, чтобы начать игру!', (self.scr.get_width() // 2, 600), self.font, self.hide_resolution_options)
        self.show_resolution = False

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            pygame.mixer.music.set_volume(100)  
        else:
            pygame.mixer.music.set_volume(0)  
        self.save_settings()  
        self.settings_buttons[0].text = f'Звук: {"Включен" if self.sound_on else "Выключен"}' 

    def show_resolution_options(self):
        self.show_resolution = True

    def hide_resolution_options(self):
        self.show_resolution = False

    def change_resolution(self, width, height):
        self.current_resolution = (width, height)
        self.scr = pygame.display.set_mode((width, height))
        self.save_settings() 
    
    def new_game(self):
        self.controls_showing = True
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
    
    def handle_mouse_click(self, pos: tuple[int, int]):
        if self.show_settings:
            if self.show_resolution:  
                for button in self.resolution_buttons:
                    if button.is_clicked(pos):
                        button.on_click()
                        break
            else: 
                for button in self.settings_buttons:
                    if button.is_clicked(pos):
                        button.on_click()
                        break
        else: 
            for button in self.buttons:
                if button.is_clicked(pos):
                    button.on_click()
                    break

    def handle_mouse_motion(self, pos):
        if self.show_settings:
            if self.show_resolution:  
                for button in self.resolution_buttons:
                    button.on_hover(button.is_clicked(pos))
            else: 
                for button in self.settings_buttons:
                    button.on_hover(button.is_clicked(pos))
        else:  
            for button in self.buttons:
                button.on_hover(button.is_clicked(pos))

            
    def update(self):
        """Main update loop for handling the menu and buttons."""
        if self.show_settings:
            if self.show_resolution:
                for button in self.resolution_buttons:
                    button.update()
            else:
                for button in self.settings_buttons:
                    button.update()
        else:
            for button in self.buttons:
                button.update()
    
    def draw(self):
        self.scr.fill((128, 128, 255))
        
        self.scroll_background()

        if self.show_settings:
            if self.show_resolution:
                for button in self.resolution_buttons:
                    button.draw(self.scr)
                    # button.rect.x = self.scr.get_width() // 2
                    button.position = (self.scr.get_width()//2, button.position[1])
            else:
                for button in self.settings_buttons:
                    button.draw(self.scr)
                    button.position = (self.scr.get_width()//2, button.position[1])
        elif self.controls_showing:
            self.render_text2("Привет! Ты начинаешь новое сохранение.", (self.scr.get_width()//2, 200))
            self.render_text2("Для движения используй клавиши стрелок или WASD.", (self.scr.get_width()//2, 250))
            self.render_text2("Для выбора интересующего предмета - прыгни под ним!", (self.scr.get_width()//2, 300))
            self.render_text2("А чтобы поговорить с грифонами, подойди к ним и нажми Е!", (self.scr.get_width()//2, 350))
            self.render_text2("При решении задач вводи свой ответ в поле внизу.", (self.scr.get_width()//2, 400))
            self.render_text2("Это всё! Желаем найти тебе профессию мечты!", (self.scr.get_width()//2, 450))
            self.control_button.draw(self.scr)
        else:
            for button in self.buttons:
                button.draw(self.scr)
                button.position = (self.scr.get_width()//2, button.position[1])

        self.render_title_text("Мир грифонов", (self.scr.get_width() // 2, 100))

    def render_title_text(self, text, position):
        text_surface = self.titlefont.render(text, True, (255, 255, 255)) 
        text_rect = text_surface.get_rect(center=position) 
        self.scr.blit(text_surface, text_rect)

    def render_text2(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))  
        text_rect = text_surface.get_rect(center=position)  
        self.scr.blit(text_surface, text_rect) 
        
    def render_text(self, text, position):
        text_surface = self.smallfont.render(text, True, (255, 255, 255))  
        text_rect = text_surface.get_rect(topleft=position)  
        self.scr.blit(text_surface, text_rect) 
        
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

        self.scr.blit(self.bg_image2, (self.bg_scroll2, self.scr.get_height() - self.bg_image2.get_height() - 160))
        self.scr.blit(self.bg_image2, (self.bg_scroll2 + self.bg_image2.get_width(), self.scr.get_height() - self.bg_image2.get_height() - 160))

        self.scr.blit(self.bg_image1, (self.bg_scroll1, self.scr.get_height() - self.bg_image1.get_height()))
        self.scr.blit(self.bg_image1, (self.bg_scroll1 + self.bg_image1.get_width(), self.scr.get_height() - self.bg_image1.get_height()))