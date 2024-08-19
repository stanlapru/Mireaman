import pygame
import random
import math
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
        self.amplitude = 50  # Amplitude for sine wave
        self.frequency = 0.005  # Frequency for sine wave
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./resources/audio/music/dialog1-loop.mp3")
        pygame.mixer.music.play(-1)
        self.setup_sprites()

    def setup_sprites(self):
        # Create sprites that move from right to left   
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load('./resources/textures/portal/line-long.png').convert_alpha()
        sprite.rect = sprite.image.get_rect(center=(self.screen.get_width(), random.randint(100, self.screen.get_height() - 100)))
        sprite.speed = random.randint(5, 10)  # Random speed for each sprite

        sprite2 = pygame.sprite.Sprite()
        sprite2.image = pygame.image.load('./resources/textures/portal/line-medium.png').convert_alpha()
        sprite2.rect = sprite.image.get_rect(center=(self.screen.get_width(), random.randint(100, self.screen.get_height() - 100)))
        sprite2.speed = random.randint(5, 10)  # Random speed for each sprite

        sprite3 = pygame.sprite.Sprite()
        sprite3.image = pygame.image.load('./resources/textures/portal/line-short.png').convert_alpha()
        sprite3.rect = sprite.image.get_rect(center=(self.screen.get_width(), random.randint(100, self.screen.get_height() - 100)))
        sprite3.speed = random.randint(5, 10)  # Random speed for each sprite

        sprite4 = pygame.sprite.Sprite()
        sprite4.image = pygame.image.load('./resources/textures/portal/star.png').convert_alpha()
        sprite4.rect = sprite.image.get_rect(center=(self.screen.get_width(), random.randint(100, self.screen.get_height() - 100)))
        sprite4.speed = random.randint(5, 10)  # Random speed for each sprite
        self.sprites.add(sprite)
        self.sprites.add(sprite2)
        self.sprites.add(sprite3)
        self.sprites.add(sprite4)

        # Create a sprite that moves in a sine wave
        self.sine_sprite = pygame.sprite.Sprite()
        self.sine_sprite.image = pygame.image.load('./resources/textures/player/right_idle/right1.png').convert_alpha()
        self.sine_sprite.rect = self.sine_sprite.image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.sine_sprite.initial_x = self.sine_sprite.rect.x
        
        self.sprites.add(self.sine_sprite)

    def interpolate_color(self, start_color, end_color, factor):
        return (
            start_color.r + (end_color.r - start_color.r) * factor,
            start_color.g + (end_color.g - start_color.g) * factor,
            start_color.b + (end_color.b - start_color.b) * factor,
        )

    def move_sprites(self):
        for sprite in self.sprites:
            # Move sprites from right to left
            if sprite not in [self.sine_sprite]:
                sprite.rect.x -= sprite.speed

                # If the sprite moves off the left side of the screen
                if sprite.rect.right < 0:
                    # Teleport it back to the right side with a random y position
                    sprite.rect.left = self.screen.get_width()
                    sprite.rect.y = random.randint(100, self.screen.get_height() - 100)

            # Move the sine wave sprite
            elif sprite.rect.centerx == self.screen.get_width() // 2:
                time_offset = pygame.time.get_ticks()
                sprite.rect.y = self.screen.get_height() // 2 + self.amplitude * math.sin(self.frequency * (time_offset))

    def run(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        factor = min(elapsed_time / self.duration, 1)

        current_color = self.interpolate_color(self.start_color, self.end_color, factor)
        self.screen.fill(current_color)

        # Move and draw sprites
        self.move_sprites()
        self.sprites.draw(self.screen)

        # Transition to the next screen after the duration
        if elapsed_time >= self.duration:
            self.done = True