import pygame


class InteractableObject(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, object_id, initial_image, interacted_image, obj_id_rus):
        super().__init__(groups)
        self.object_id = object_id
        self.obj_id_rus = obj_id_rus
        self.initial_image = pygame.transform.scale(pygame.image.load(initial_image).convert_alpha(), (48, 48))
        self.image = pygame.transform.scale(pygame.image.load(initial_image).convert_alpha(), (48, 48))
        self.rect = self.image.get_rect(topleft=pos)
        print(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        self.hitbox = self.rect.inflate(-10, -10)  # Adjust hitbox size if needed
        self.interacted_image = pygame.transform.scale(pygame.image.load(interacted_image).convert_alpha(), (48,48))
        self.interacted = False

        # Add to the obstacle group for collision detection
        self.obstacle_sprites = obstacle_sprites
        self.obstacle_sprites.add(self)
        
        print(object_id, self.rect.x, self.rect.y)

    def interact(self):
        if not self.interacted:
            self.image = self.interacted_image
            self.interacted = True
        else:
            self.image = self.initial_image
            self.interacted = False
        return self.object_id
    
    def is_hovered(self, mouse_pos):
        """Returns True if the mouse is hovering over the object."""
        print(self.object_id)
        return self.rect.collidepoint(mouse_pos)