import pygame
from button import Button

class MainScreen:
    def __init__(self, game):
        self.game = game
        pygame.font.init()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        MENU_BUTTON = Button(150, 150, 150, 50, (255, 250, 250),
          (255, 0, 0), "TimesNewRoman",
          (255, 255, 255), "Main Menu")
        CONTROL_BUTTON = Button(150, 150, 150, 50,
            (0, 0, 0), (0, 0, 255),
            "TimesNewRoman",
            (255, 255, 255), "Back")

    def handle_mouse_click(self, pos):
        # Check if the click is within a certain region on the screen
        # If yes, switch to the second screen
        if 100 < pos[0] < 200 and 100 < pos[1] < 200:
            self.game.switch_screen(self.game.second_screen)

    def draw(self, screen):
        screen.fill((128, 128, 255))  # Clear the screen
        self.render_text("Моя Игра №12 - ПД:ЦО", (screen.get_width() // 2, screen.get_height() // 2), screen)
        self.render_text("Нажмите чтобы начать!", (screen.get_width() // 2, screen.get_height() // 2 + 40), screen)

    def render_text(self, text, position, screen):
        text_surface = self.font.render(text, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect(center=position)  # Center the text
        screen.blit(text_surface, text_rect)  # Blit the text onto the screen


    def update(selfs):
        pass
