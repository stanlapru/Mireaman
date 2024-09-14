import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, data):
        super().__init__()
        # Load the idle image first
        self.original_image = pygame.image.load('./resources/textures/player/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (
            self.original_image.get_width() // 2, self.original_image.get_height() // 2))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-16, -16)  # Smaller hitbox for more precise collision

        # Animation setup
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index = 0
        self.animation_speed = 0.15

        # Player movement
        self.direction = pygame.math.Vector2()
        self.speed = 2

        # Interaction and dialog
        self.interacting = False
        self.dialog_active = False
        self.interact_cd = 200
        self.interact_time = None

        # Obstacles
        self.obstacle_sprites = obstacle_sprites
        self.data = data

    def import_player_assets(self):
        character_path = './resources/textures/player/'
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

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'interact' in self.status:
                self.status = self.status + '_idle'

    def animate(self):
        """Animate the player based on current status."""
        animation = self.animations[self.status]
        
        # Increment frame index for animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image to the current frame
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def input(self, npcs):
        """Handle player input (movement and interaction)."""
        # if self.dialog_active:  # Block input when dialog is active
        #     self.direction.x = 0
        #     self.direction.y = 0
        #     return

        keys = pygame.key.get_pressed()

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # Interaction (press 'E')
        if keys[pygame.K_e] and not self.interacting:
            for npc in npcs:
                if npc.player_nearby:  # Check if an NPC is nearby
                    self.interacting = True  # Start interaction
                    npc.interacting = True  # Let the NPC know the interaction started
                    self.dialog_active = True  # Show dialog
                    self.direction.x = 0
                    self.direction.y = 0
                    break
        elif not keys[pygame.K_e]:
            self.interacting = False
        
        if keys[pygame.K_EQUALS]:
            self.hitbox.x = 528
            self.hitbox.y = 678

    def move(self, speed):
        """Move the player, handling collisions."""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move horizontally first
        self.hitbox.x += self.direction.x * speed
        self.data['pos_x'] = self.hitbox.x
        self.collision('horizontal')

        # Move vertically
        self.hitbox.y += self.direction.y * speed
        self.data['pos_y'] = self.hitbox.y
        self.collision('vertical')

        # Update rect based on hitbox
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Handle collisions in the given direction."""
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom

    def cooldowns(self):
        # """Handle cooldowns for interaction."""
        # current_time = pygame.time.get_ticks()
        # if self.interacting:
        #     if current_time - self.interact_time >= self.interact_cd:
        #         self.interacting = False
        pass

    def update(self):
        """Update the player state each frame."""
        #self.input(npcs)
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)