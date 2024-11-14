import pygame
from settings import *
from interactable import InteractableObject
from support import import_folder

class NPCPlatformer(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, texture, dialog_id):
        super().__init__(groups)
        self.image = pygame.image.load(texture).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-22,-0)
        self.texture_path = texture
        self.dialog_id = dialog_id
        
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        
  
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.gravity = 0.1
        self.vertical_vel = 0
        self.interacting = False
        self.interact_cd = 200
        self.interact_time = None
        self.colliding = False
        self.falling = False
        
        self.interact_distance = 30
        self.obstacle_sprites = obstacle_sprites
        
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.show_interact_text = False
        
    def import_player_assets(self):
        character_path = self.texture_path[:-15]
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[], 
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
        }
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = self.scale_animation_frames(import_folder(full_path))
            
    def scale_animation_frames(self, frames):
        scaled_frames = []
        for frame in frames:
            scaled_frame = pygame.transform.scale(frame, (frame.get_width(), frame.get_height()))
            scaled_frames.append(scaled_frame)
        return scaled_frames
    
    def check_proximity(self, player_pos):
        distance = pygame.math.Vector2(self.rect.center).distance_to(player_pos)
        if distance < self.interact_distance: 
            self.player_nearby = True
        else:
            self.player_nearby = False

    def draw_interact_text(self, display_surface):
        """Draw the 'Interact' text above the NPC."""
        if self.player_nearby and not self.interacting:
            interact_text = self.font.render('[E]', True, (255, 255, 255))  
            display_surface.blit(interact_text, (display_surface.get_width() // 2, display_surface.get_height() // 2 - 50))
                
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'interact' in self.status:
                self.status = self.status + '_idle'
    
    def animate(self):
        animation = self.animations[self.status]
        
        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
            
    def update(self, player_pos):
        self.get_status()
        self.animate()
        self.check_proximity(player_pos)
        