import os
import pygame
from player import Player

class WorldScreen:
    def __init__(self, game, screen: pygame.Surface):
        self.game = game
        self.screen = screen
        
    def update(self, events):
        self.handle_events(events)
        self.update_camera()
    
    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     self.player.move_left()
        # elif keys[pygame.K_RIGHT]:
        #     self.player.move_right()
        # elif keys[pygame.K_x]:
        #     self.player.jump()
        # else:
        #     self.player.stop_movement()

        # for event in events:
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE or event.key == pygame.K_x:
        #             self.player.jump()
        #     elif event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT and self.player.vel_x < 0:
        #             self.player.stop_movement()
        #         elif event.key == pygame.K_RIGHT and self.player.vel_x > 0:
        #             self.player.stop_movement()
        #         elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
        #             self.player.stop_jump()

    def update_camera(self):
        i = 0
        # Center the camera on the player horizontally
        # player_center_x = self.player.rect.centerx
        # screen_center_x = self.camera_offset_x + self.camera_margin_x

        # if player_center_x > screen_center_x:
        #     # print('doing the right')
        #     self.camera_offset_x = min(self.camera_offset_x + (player_center_x - screen_center_x), self.world_width - 640)
        # elif player_center_x < screen_center_x:
        #     # print('doing the left')
        #     self.camera_offset_x = max(self.camera_offset_x - (screen_center_x - player_center_x), 0)

    def draw(self, screen):
        screen.fill((255, 0, 255))
        #screen.blit(self.background, (-self.camera_offset_x, 0))  # Draw the background image with camera offset

        # Draw environment and player with camera offset
        # for platform in self.environment.platforms:
        #     platform.draw(screen, self.camera_offset_x)
            
        # for box in self.environment.boxes:
        #     box.draw(screen, self.camera_offset_x)

       # Remove the player from the environment group before drawing
       #