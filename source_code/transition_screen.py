import pygame
from button import Button

class PortalScreen:
    def __init__(self, screen):
        self.screen = screen
        self.start_time = pygame.time.get_ticks()  # Start time for the transition
        self.duration = 6000  # Duration of the transition in milliseconds (3 seconds)
        self.start_color = pygame.Color('maroon')
        self.end_color = pygame.Color('#2E2E2E')  # Darker tint
        self.sprites = pygame.sprite.Group()
        self.done = False
        self.setup_sprites()

    def setup_sprites(self):
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = pygame.image.load('./resources/textures/portal/line-long.png').convert_alpha()
        sprite1.rect = sprite1.image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.sprites.add(sprite1)

        sprite2 = pygame.sprite.Sprite()
        sprite2.image = pygame.image.load('./resources/textures/portal/line-short.png').convert_alpha()
        sprite2.rect = sprite2.image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.sprites.add(sprite2)

    def interpolate_color(self, start_color, end_color, factor):
        # Linear interpolation of color
        return (
            start_color.r + (end_color.r - start_color.r) * factor,
            start_color.g + (end_color.g - start_color.g) * factor,
            start_color.b + (end_color.b - start_color.b) * factor,
        )

    def run(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        factor = min(elapsed_time / self.duration, 1)  # Ensure factor stays between 0 and 1

        # Interpolate between the start and end colors based on the elapsed time
        current_color = self.interpolate_color(self.start_color, self.end_color, factor)
        self.screen.fill(current_color)

        # Draw sprites
        self.sprites.draw(self.screen)

        # Transition to the next screen after the duration
        if elapsed_time >= self.duration:
            self.done = True