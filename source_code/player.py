import pygame
from bullet import Bullet
import os
import sys

def load_image(name, colokey=None):
    fullname = os.path.join('resources/textures', name)
    if not os.path.isfile(fullname):
        print('not found', fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colokey is not None:
        image = image.convert()
        if colokey == -1:
            colokey = image.get_at((0, 0))
        image.set_colorkey(colokey)
    return fullname

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_sheet_path = load_image('mireaman/sprites.png')  # Get the file path
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.image = self.get_sprite(0, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.jumping = False
        self.bullets = pygame.sprite.Group()
        self.direction = "right"
        self.animation_frame = 0
        self.animation_state = "idle"

    def update(self, platforms):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.check_collision(platforms, "x")
        self.rect.y += self.vel_y
        self.check_collision(platforms, "y")
        self.bullets.update()
        self.update_animation()

    def apply_gravity(self):
        self.vel_y += self.gravity

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vel_y = self.jump_power

    def stop_jump(self):
        if self.jumping and self.vel_y < -3:
            self.vel_y = -3

    def check_collision(self, platforms, axis):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if axis == "x":
                    if self.vel_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0:  # Moving left
                        self.rect.left = platform.rect.right
                elif axis == "y":
                    if self.vel_y > 0:  # Moving downward
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.jumping = False
                    elif self.vel_y < 0:  # Moving upward
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0
    
    def update_animation(self):
        if self.jumping:
            self.animation_state = "jumping"
        elif self.vel_x != 0:
            self.animation_state = "movement"
        else:
            self.animation_state = "idle"

        self.animation_frame = (self.animation_frame + 1) % 7  # Cycle through frames
        self.image = self.get_sprite(self.animation_frame, self.get_animation_row())

    def get_animation_row(self):
        if self.animation_state == "idle":
            return 0
        elif self.animation_state == "jumping":
            return 1
        else:
            return 2

    def get_sprite(self, frame, row):
        sprite_width = 34
        sprite_height = 46
        x = frame * sprite_width
        y = row * sprite_height
        return self.sprite_sheet.subsurface((x, y, sprite_width, sprite_height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery, self.direction)  # Create a bullet
        self.bullets.add(bullet)  # Add bullet to group
        
    def move_left(self):
        self.vel_x = -5
        self.direction = "left"  # Update direction when moving left

    def move_right(self):
        self.vel_x = 5
        self.direction = "right"
