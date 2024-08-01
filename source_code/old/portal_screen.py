import pygame
from button import Button

class PortalScreen:
    def __init__(self, game):
        self.game = game
        pygame.font.init()
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)

    def draw(self, screen):
        screen.fill((128, 128, 255))  # Clear the screen
        self.render_text("Экран портала", (screen.get_width() // 2, screen.get_height() // 2), screen)
        self.render_text("На этом всё", (screen.get_width() // 2, screen.get_height() // 2 + 40), screen)

    def render_text(self, text, position, screen):
        text_surface = self.font.render(text, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect(center=position)  # Center the text
        screen.blit(text_surface, text_rect)  # Blit the text onto the screen


    def update(selfs):
        pass
