import pygame


class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, object_id, initial_image, interacted_image):
        super().__init__(groups)
        self.object_id = object_id
        self.image = pygame.image.load(initial_image).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)  # Adjust hitbox size if needed
        self.interacted_image = pygame.image.load(interacted_image).convert_alpha()
        self.interacted = False

    def interact(self, player):
        if not self.interacted and self.hitbox.colliderect(player.hitbox):
            self.image = self.interacted_image
            self.interacted = True
            return self.object_id
        return None