import pygame
from player import Player
from portal import Portal
from lesson_box import LessonBox

class StartScreen:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.player = Player(30, 380, screen)
        self.portal = Portal(1520, 360, 50, 100)
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

        # Create environment
        self.environment = pygame.sprite.Group()
        for key, value in self.lesson_dict.items():
             LessonBox(50+key*150, 300, 40, 40, value['path'], key, self.environment)
        # self.environment.add_platform(0, 20, 620, 20)  # Example top
        #self.environment.add_platform(-20, 0, 20, 620)   # Example left wall
        #self.environment.add_platform(1600, 20, 20, 620) # Example right wall

        self.background = pygame.image.load("resources/textures/environment/intro.png").convert()

        self.player_speed = 5

        # Camera properties
        self.camera_offset_x = 0
        self.camera_margin_x = 640 // 2
        self.world_width = 1600  # Example world width limit

    def update(self, events):
        self.handle_events(events)
        #self.player.update(self.environment.platforms, self.environment.boxes, self.portal)
        
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
        # for platform in self.environment.platforms:
        #     platform.draw(screen, self.camera_offset_x)
            
        # for box in self.environment.boxes:
        #     box.draw(screen, self.camera_offset_x)

        self.environment.draw(self.screen)

        self.portal.draw(screen, self.camera_offset_x)
        self.player.draw(screen, self.camera_offset_x)
        # self.player.bullets.draw(screen)
