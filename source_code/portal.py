import pygame
import json
import time

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.image = pygame.image.load('./resources/textures/portal/portal.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        self.player = player
        self.hitbox = self.rect.inflate(-10, -10)
        self.animation_timer = 0
        self.rotation_angle = 0
        self.touched = False
        self.savedata = {
            'pos_x': 1200,
            'pos_y': 1300,
            'subjects': self.player.selected_objects,
            'fps': 60,
            'demo_mode': False,
            'width': 1280,
            'height': 720,
        }

    def save_selected_subjects(self):
        with open('./data/savedata.json', 'w') as file:
            json.dump(self.savedata, file)

    def check_collision(self):
        if self.rect.colliderect(self.player.rect) and len(self.player.selected_objects) != 0:
            self.touched = True

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > 500:  # Rotate every 0.5 seconds
            self.rotation_angle = (self.rotation_angle + 180) % 360
            self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
            self.rect = self.image.get_rect(center=self.rect.center)  # Keep the position
            self.animation_timer = current_time

    def update(self):
        self.animate()
        self.check_collision()
