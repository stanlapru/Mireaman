import pygame
from settings import *
from support import import_folder

class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, groups, data, interact_distance=30):
        super().__init__(groups)
        self.image = pygame.image.load('./resources/textures/npc/1/down_idle/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-22,-22)
        
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.05
  
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.interacting = False
        self.interact_cd = 200
        self.interact_time = None
        
        self.data = data

        self.interact_distance = interact_distance  # Distance to interact
        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)
        self.show_interact_text = False

        # Load arrow image
        #self.arrow_image = pygame.image.load('./resources/textures/player/arrow.jpg').convert_alpha()
        #self.arrow_rect = self.arrow_image.get_rect(center=self.rect.center)
        self.arrow_visible = False  # Flag to indicate if arrow should be displayed

        
    def import_player_assets(self):
        character_path = './resources/textures/npc/1/'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[], 
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
        }
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = self.scale_animation_frames(import_folder(full_path))

    def scale_animation_frames(self, frames):
        """Scale all animation frames down by a factor of 3."""
        scaled_frames = []
        for frame in frames:
            scaled_frame = pygame.transform.scale(frame, (frame.get_width() // 3, frame.get_height() // 3))
            scaled_frames.append(scaled_frame)
        return scaled_frames
    
    def check_proximity(self, player_pos):
        """Check if player is close enough to interact."""
        distance = pygame.math.Vector2(self.rect.center).distance_to(player_pos)
        self.show_interact_text = distance < self.interact_distance

    def draw_interact_text(self, display_surface):
        """Draw the 'Interact' text above the NPC."""
        if self.show_interact_text:
            interact_text = self.font.render('Поговорить', True, (255, 255, 255))  # White text
            display_surface.blit(interact_text, (self.rect.centerx * 2, self.rect.top))
            
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

    def draw(self, surface):
        """Draw player or arrow based on visibility."""
        if self.arrow_visible:
            surface.blit(self.arrow_image, self.arrow_rect)
        else:
            surface.blit(self.image, self.rect)