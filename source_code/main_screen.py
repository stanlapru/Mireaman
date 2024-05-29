import pygame
from button import Button

class MainScreen:
    def __init__(self, game: pygame.Surface):
        self.game = game
        pygame.font.init()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)

    def handle_mouse_click(self, pos: tuple[int, int]):
        # Check if the click is within a certain region on the screen
        # If yes, switch to the second screen
        if 100 < pos[0] < 200 and 100 < pos[1] < 200:
            self.game.switch_screen(self.game.second_screen)

    def draw(self):
        self.game.fill((128, 128, 255))  # Clear the screen
        self.render_text("Моя Игра №12 - ПД:ЦО", (self.game.get_width() // 2, self.game.get_height() // 2))
        self.render_text("Нажмите чтобы начать!", (self.game.get_width() // 2, self.game.get_height() // 2 + 40))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect(center=position)  # Center the text
        self.game.blit(text_surface, text_rect)  # Blit the text onto the screen


    def update(selfs):
        pass