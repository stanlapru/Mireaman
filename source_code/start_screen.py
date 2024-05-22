import pygame
from environment import Environment
from player import Player
from portal import Portal

class StartScreen:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.player = Player(30, 380, screen)
        self.portal = Portal(1520, 360, 50, 100)

        # Create environment
        self.environment = Environment()
        self.environment.add_platform(0, 480, 1620, 20)  # Example floor
        # self.environment.add_platform(0, 20, 620, 20)  # Example top
        self.environment.add_platform(-20, 0, 20, 620)   # Example left wall
        self.environment.add_platform(1600, 20, 20, 620) # Example right wall
        
        self.environment.add_box4(50,320)
        self.environment.add_box5(200,320)
        self.environment.add_box6(350,320)
        self.environment.add_box7(500,320)
        
        self.environment.add_box(630,320)
        self.environment.add_box2(730,320)
        self.environment.add_box3(830,320)
        self.environment.add_box8(930,320)
        
        self.environment.add_box9(1130,320)
        self.environment.add_box10(1330,320)

        self.background = pygame.image.load("resources/textures/environment/intro.png").convert()

        self.player_speed = 5

        # Camera properties
        self.camera_offset_x = 0
        self.camera_margin_x = 640 // 2
        self.world_width = 1600  # Example world width limit

    def update(self, events):
        self.handle_events(events)
        self.player.update(self.environment.platforms, self.environment.boxes, self.portal)
        self.update_camera()

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        elif keys[pygame.K_x]:
            self.player.jump()
        else:
            self.player.stop_movement()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_x:
                    self.player.jump()
                elif event.key == pygame.K_z:
                    self.player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.vel_x < 0:
                    self.player.stop_movement()
                elif event.key == pygame.K_RIGHT and self.player.vel_x > 0:
                    self.player.stop_movement()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
                    self.player.stop_jump()

    def update_camera(self):
        # Center the camera on the player horizontally
        player_center_x = self.player.rect.centerx
        screen_center_x = self.camera_offset_x + self.camera_margin_x

        if player_center_x > screen_center_x:
            # print('doing the right')
            self.camera_offset_x = min(self.camera_offset_x + (player_center_x - screen_center_x), self.world_width - 640)
        elif player_center_x < screen_center_x:
            # print('doing the left')
            self.camera_offset_x = max(self.camera_offset_x - (screen_center_x - player_center_x), 0)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.background, (-self.camera_offset_x, 0))  # Draw the background image with camera offset

        # Draw environment and player with camera offset
        for platform in self.environment.platforms:
            platform.draw(screen, self.camera_offset_x)
            
        for box in self.environment.boxes:
            box.draw(screen, self.camera_offset_x)

        self.portal.draw(screen, self.camera_offset_x)
        self.player.draw(screen, self.camera_offset_x)
        self.player.bullets.draw(screen)

