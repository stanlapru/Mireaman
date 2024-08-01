import pygame
import pygame_gui
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

    def show_pause(self):
        pass
		
    def display(self):
        self.show_pause()
        # self.selection_box(80,635) # magic