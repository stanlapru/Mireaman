import pygame

class MenuButton:
    def __init__(self, text, position, font, callback, color=(255,255,255), hover_color=(255,255,0)):
        self.text = text
        self.position = position
        self.font = font
        self.callback = callback
        self.normal_color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text_surface = self.font.render(self.text, True, self.current_color)
        self.rect = self.text_surface.get_rect(center=self.position)

    def draw(self, surface):
        self.text_surface = self.font.render(self.text, True, self.current_color)
        self.rect = self.text_surface.get_rect(center=self.position)
        surface.blit(self.text_surface, self.rect)
        
    def on_hover(self, is_hovering):
        self.current_color = self.hover_color if is_hovering else self.normal_color

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def on_click(self):
        self.callback()