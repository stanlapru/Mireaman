import pygame
from environment import Environment
from player import Player

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ПД")

# Colors
WHITE = (255, 255, 255)

# Create player
player = Player(100, 100)

# Create environment
environment = Environment()
environment.add_platform(0, 460, 620, 20)  # Example floor
environment.add_platform(0, 20, 620, 20)  # Example top
environment.add_platform(0, 20, 20, 620)   # Example left wall
environment.add_platform(620, 20, 20, 620) # Example right wall

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()
            elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
                player.jump()  
            elif event.key == pygame.K_z: 
                player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.vel_x < 0:
                player.vel_x = 0
            elif event.key == pygame.K_RIGHT and player.vel_x > 0:
                player.vel_x = 0
            elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
                player.stop_jump()
    # Update player
    player.update(environment.platforms)

    # Draw environment and player
    environment.draw(screen)
    player.draw(screen)
    player.bullets.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Cap at 60 FPS

pygame.quit()