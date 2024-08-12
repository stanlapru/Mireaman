import pygame


class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, object_id, initial_image, interacted_image):
        super().__init__(groups)
        self.object_id = object_id
        self.initial_image = pygame.transform.scale(pygame.image.load(initial_image).convert_alpha(), (64, 64))
        self.image = pygame.transform.scale(pygame.image.load(initial_image).convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)  # Adjust hitbox size if needed
        self.interacted_image = pygame.transform.scale(pygame.image.load(interacted_image).convert_alpha(), (64,64))
        self.interacted = False

        # Add to the obstacle group for collision detection
        self.obstacle_sprites = obstacle_sprites
        self.obstacle_sprites.add(self)

    def interact(self):
        if not self.interacted:
            self.image = self.interacted_image
            self.interacted = True
            return self.object_id
        else:
            self.image = self.initial_image
            self.interacted = False
            return None
