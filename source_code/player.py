import pygame
from bullet import Bullet
import os
import sys
from portal_screen import PortalScreen
from lesson_box import LessonBox
from platform_collision import PlatformCollision

def load_image(name, colorkey=None):
    fullname = os.path.join('resources/textures', name)
    if not os.path.isfile(fullname):
        print('not found', fullname)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, texture, width, height, *group):
        super().__init__(*group)
        self.sprite_sheet_path = "mireaman/sprites.png"
        self.sprite_sheet = load_image(self.sprite_sheet_path)
        self.image = pygame.transform.scale(pygame.image.load(texture), (width, height))
        self.rect = self.image.get_rect()
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
        self.portal_touched = False


    # обновление позиции игрока
    def update(self, environment, portal):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.check_collision(environment, portal, "x")
        self.rect.y += self.vel_y
        self.check_collision(environment, portal, "y")
        self.frame_counter += 1
        print(self.frame_counter, self.rect.topleft)

    # гравитация
    def apply_gravity(self): # Сломано, почему???????????
        self.vel_y += self.gravity
        if self.vel_y > 10:
            self.vel_y = 10
        if self.vel_y < -10:
            self.vel_y = -10

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vel_y = -self.jump_power

    def stop_jump(self):
        if self.jumping and self.vel_y < -3:
            self.vel_y = -3

    def stop_movement(self):
        self.vel_x = 0
        
    def move_right(self):
        self.vel_x = -5
        self.direction = "right"
        
    def move_left(self):
        self.vel_x = 5
        self.direction = "left"

    def check_collision(self, environment, portal, axis):
        for entity in environment:
            if self.rect.colliderect(entity.rect):
                if isinstance(entity, LessonBox) or isinstance(entity, PlatformCollision):
                    entity.selected = True
                if axis == "x":
                    if self.vel_x > 0:
                        self.rect.right = entity.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = entity.rect.right
                elif axis == "y":
                    if self.vel_y > 0:
                        self.rect.bottom = entity.rect.top
                        self.vel_y = 0
                        self.jumping = False
                    elif self.vel_y < 0:
                        self.rect.top = entity.rect.bottom
                        self.vel_y = 0
                        
        if self.rect.colliderect(portal.rect):
            self.portal_touched = True


    # def update_animation(self, direction):
    #     if self.jumping:
    #         self.animation_state = "jumping"
    #     elif self.vel_x != 0:
    #         self.animation_state = "movement"
    #     else:
    #         self.animation_state = "idle"

    #     self.frame_counter += 1
    #     if self.frame_counter >= self.frame_delay:
    #         self.animation_frame = (self.animation_frame + 1) % 3  # 7 frames per animation
    #         self.frame_counter = 0

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

    def draw(self, surface, camera_offset_x):
        sprite, sprite_size = self.get_sprite(self.animation_frame, self.get_animation_row(), self.direction)
        surface.blit(sprite, (self.rect.x - camera_offset_x, self.rect.y))
