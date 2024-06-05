import pygame
from player import Player
from portal import Portal
from lesson_box import LessonBox
from platform_collision import PlatformCollision

class StartScreen:
    def __init__(self, game, screen: pygame.Surface):
        self.game = game
        self.screen = screen
        self.portal = Portal(self.screen.get_width()-80, 360, 50, 100)
        self.lesson_dict = {0: {'name': 'Литература', 'path': 'resources/textures/blocks/literature.png'},
                            1: {'name': 'География', 'path': 'resources/textures/blocks/geography.png'},
                            2: {'name': 'Обществознание', 'path': 'resources/textures/blocks/social.png'},
                            3: {'name': 'Русский', 'path': 'resources/textures/blocks/russian.png'},
                            4: {'name': 'Математика', 'path': 'resources/textures/blocks/math.png'},
                            5: {'name': 'Физика', 'path': 'resources/textures/blocks/physics.png'},
                            6: {'name': 'Иностранный язык', 'path': 'resources/textures/blocks/language.png'},
                            7: {'name': 'Программирование', 'path': 'resources/textures/blocks/coding.png'},
                            8: {'name': 'Химия', 'path': 'resources/textures/blocks/chemistry.png'},
                            9: {'name': 'Биология', 'path': 'resources/textures/blocks/biology.png'},
                            }

        self.font = pygame.font.Font('resources/fonts/pixeloidSans.ttf', 36)

        # Create environment
        self.environment = pygame.sprite.Group()
        for key, value in self.lesson_dict.items():
             LessonBox(50+key*150, 300, 40, 40, value['path'], key, self.environment)
        # self.environment.add_platform(0, 20, 620, 20)  # Example top
        # self.environment.add_platform(-20, 0, 20, 620)   # Example left wall
        # self.environment.add_platform(1600, 20, 20, 620) # Example right wall

        self.player = Player(50, 400, 'resources/textures/mireaman/sprites.png', 60, 60, self.environment)

        PlatformCollision(0, 500, 1800, 20, self.environment)
        PlatformCollision(0, 0, 20, 800, self.environment)
        PlatformCollision(1780, 0, 20, 800, self.environment)

        self.background = pygame.image.load("resources/textures/environment/intro.png").convert()

        # Camera properties
        self.camera_offset_x = 0
        self.camera_margin_x = self.screen.get_width() // 2
        self.world_width = self.screen.get_width()
        self.portal_touched = False

    def update(self, events):
        self.handle_events(events)
        self.portal_touched = self.player.portal_touched
        self.player.update(self.environment, self.portal)
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
        # for platform in self.environment.platforms:
        #     platform.draw(screen, self.camera_offset_x)
            
        # for box in self.environment.boxes:
        #     box.draw(screen, self.camera_offset_x)

       # Remove the player from the environment group before drawing
        self.environment.remove(self.player)
        
        # Draw the environment without the player
        self.custom_draw(self.environment, screen)
        
        # Draw the player separately with camera offset
        self.player.draw(screen, self.camera_offset_x)
        
        # Add the player back to the environment group
        self.environment.add(self.player)

        self.portal.draw(screen, self.camera_offset_x)
        # self.player.bullets.draw(screen)

        self.render_text("Position: "+', '.join(tuple(str(i) for i in self.player.rect.center)), (200, 32))

    def custom_draw(self, sprite_group, surface):
        for sprite in sprite_group:
            if sprite != self.player:
                surface.blit(sprite.image, (sprite.rect.x - self.camera_offset_x, sprite.rect.y))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))  # Render the text
        text_rect = text_surface.get_rect(center=position)  # Center the text
        self.screen.blit(text_surface, text_rect)  # Blit the text onto the screen