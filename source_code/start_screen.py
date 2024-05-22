import pygame
from environment import Environment
from player import Player   

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.player = Player(100, 100)

        # Create environment
        self.environment = Environment()
        self.environment.add_platform(0, 460, 620, 20)  # Example floor
        self.environment.add_platform(0, 20, 620, 20)  # Example top
        self.environment.add_platform(0, 20, 20, 620)   # Example left wall
        self.environment.add_platform(620, 20, 20, 620) # Example right wall
    
    def update(self, events):
        self.player.update(self.environment.platforms)
        self.handle_events(events)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
                    self.player.jump()  
                elif event.key == pygame.K_z: 
                    self.player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.vel_x < 0:
                    self.player.vel_x = 0
                elif event.key == pygame.K_RIGHT and self.player.vel_x > 0:
                    self.player.vel_x = 0
                elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
                    self.player.stop_jump()


    def handle_mouse_click(self, pos):
        if 300 < pos[0] < 400 and 100 < pos[1] < 200:
            self.game.switch_screen(self.game.main_screen)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.environment.draw(screen)
        self.player.draw(screen)
        self.player.bullets.draw(screen)
