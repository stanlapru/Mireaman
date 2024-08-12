import pygame
from settings import *
from interactable import InteractableObject
from support import import_folder

class PlayerPlatformer(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('./resources/textures/player/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-22,-0)
        
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
        
        self.obstacle_sprites = obstacle_sprites
        
    def import_player_assets(self):
        character_path = './resources/textures/player/'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[], 
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
        }
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
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
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.colliding == True and self.falling == False:
                self.vertical_vel = -2.5
            # self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            # self.status = 'down'
        else:
            self.direction.y = 0
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
            
        # interact
        if keys[pygame.K_e] and not self.interacting:
            self.interacting = True
            self.interact_time = pygame.time.get_ticks()
            
    def move(self,speed):
        self.vertical_vel += self.gravity
        self.direction.y = self.vertical_vel
        
        # # normalize
        # if self.direction.x != 0:
        #     self.direction.x = self.direction.x / abs(self.direction.x)
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        if self.colliding == True:
            self.vertical_vel = 0

        if self.vertical_vel > 5:
            self.vertical_vel = 5
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.interacting:
            if current_time - self.interact_time >= self.interact_cd:
                self.interacting = False
        
    def collision(self,direction):
        self.colliding = False
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # P ->
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # <- P
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.colliding = True
                    if self.direction.y < 0: # P up
                        self.hitbox.top = sprite.hitbox.bottom
                        self.falling = True
                    if self.direction.y > 0: # down P
                        self.hitbox.bottom = sprite.hitbox.top
                        self.falling = False
    
    def check_interactions(self):
        for interactable in self.obstacle_sprites:
            if isinstance(interactable, InteractableObject):
                selected_object_id = interactable.interact(self)
                if selected_object_id:
                    # Add to the list of selected objects
                    self.selected_objects.append(selected_object_id)
                    # Display the object at the top of the screen
                    self.display_selected_objects()

    def display_selected_objects(self):
        y_offset = 10
        for idx, obj_id in enumerate(self.selected_objects):
            object_image = pygame.image.load(f'./resources/textures/blocks/{obj_id}.png').convert_alpha()
            self.display_surface.blit(object_image, (10 + idx * 50, y_offset))
            
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.check_interactions()