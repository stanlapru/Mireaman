import pygame

class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, frames):
        super().__init__(groups)
        self.frames = [pygame.image.load(frame['image']) for frame in frames]
        self.durations = [frame['duration'] for frame in frames]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_time = 0
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.durations[self.current_frame]:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
