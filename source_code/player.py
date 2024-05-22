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
    return image  # Return the image itself, not the full path

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet_path = "mireaman/sprites.png"
        self.sprite_sheet = load_image(self.sprite_sheet_path)
        self.rect = pygame.Rect(x, y, 34, 46)
        self.image = self.get_sprite(0, 0, direction="right")
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.jumping = False
        self.direction = "right"
        self.animation_frame = 0
        self.animation_state = "idle"
        self.frame_delay = 10  
        self.frame_counter = 0  
        self.bullets = pygame.sprite.Group()

    def update(self, platforms):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.check_collision(platforms, "x")
        self.rect.y += self.vel_y
        self.check_collision(platforms, "y")
        self.update_animation(self.direction)
        self.bullets.update()

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
                    if self.vel_x > 0:
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = platform.rect.right
                elif axis == "y":
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.jumping = False
                    elif self.vel_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0

    def update_animation(self, direction):
        if self.jumping:
            self.animation_state = "jumping"
        elif self.vel_x != 0:
            self.animation_state = "movement"
        else:
            self.animation_state = "idle"

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.animation_frame = (self.animation_frame + 1) % 3  # 7 frames per animation
            self.frame_counter = 0

    def get_sprite(self, frame, row, direction):
        sprite_width = 34
        sprite_height = 46
        x_start = frame * sprite_width
        y_start = row * sprite_height
        sprite = self.sprite_sheet.subsurface(pygame.Rect(x_start, y_start, sprite_width, sprite_height))
        
        if direction == "left":
            sprite = pygame.transform.flip(sprite, True, False)

        return sprite, sprite.get_rect().size

    def get_animation_row(self):
        if self.animation_state == "idle":
            return 0
        elif self.animation_state == "jumping":
            return 1
        else:
            return 2

    def draw(self, surface):
        sprite, sprite_size = self.get_sprite(self.animation_frame, self.get_animation_row(), self.direction)
        # Pass frame and row arguments to get_sprite method
        surface.blit(sprite, self.rect)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    def move_left(self):
        self.vel_x = -5
        self.direction = "left"

    def move_right(self):
        self.vel_x = 5
        self.direction = "right"

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery, self.direction)
        self.bullets.add(bullet)