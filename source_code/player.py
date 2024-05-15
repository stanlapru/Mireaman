import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 34))  # Placeholder image
        self.image.fill((255, 0, 0))  # Red rectangle for now
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.jumping = False

    def update(self, platforms):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.check_collision(platforms, "x")
        self.rect.y += self.vel_y
        self.check_collision(platforms, "y")

    def apply_gravity(self):
        self.vel_y += self.gravity

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.vel_y = self.jump_power

    def stop_jump(self):
        if self.jumping and self.vel_y < -3:
            self.vel_y = -3

    def check_collision(self, platforms, axis):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if axis == "x":
                    if self.vel_x > 0:  # Moving right
                        self.rect.right = platform.rect.left
                    elif self.vel_x < 0:  # Moving left
                        self.rect.left = platform.rect.right
                elif axis == "y":
                    if self.vel_y > 0:  # Moving downward
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.jumping = False
                    elif self.vel_y < 0:  # Moving upward
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
