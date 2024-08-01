import pygame
import os, sys


def load_image(name, colokey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('not found')
        sys.exit()
    image = pygame.image.load(fullname)
    if colokey is not None:
        image = image.convert()
        if colokey == -1:
            colokey = image.get_at((0, 0))
        image.set_colorkey(colokey)
    return image


class Sprites(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.rect = None
        self.pos = None
        self.frames = []

    def cut_frames(self, img, columns, rows):
        self.rect = pygame.Rect(0,0, img.get_width() // columns, img.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(img.subsurface(pygame.Rect(frame_location, self.rect.size)))
    
    def move(self, x, y):
        x_c, y_c = self.image.get_size()
        self.rect = self.image.get_rect(center=(x_c // 2, y_c // 2)).move(x, y)
        self.pos = x, y


class Mireaman(Sprites):
    image = load_image("mireaman.png")
    col = 4
    row = 4

    def __init__(self, x, y, size: tuple[int, int], *groups) -> None:
        super().__init__(*groups)

        img = pygame.transform.scale(Mireaman.image, (size[0] * Mireaman.col, size[1] * Mireaman.row))
        self.cut_frames(img, Mireaman.col, Mireaman.row)

        self.cur_frames = 0
        self.image = self.frames[self.cur_frames]
        self.rect = self.rect.move(x,y)
        self.pos = x, y

        self.dict_move = {
            pygame.K_a: False,
            pygame.K_s: False,
            pygame.K_w: False,
            pygame.K_d: False,
        }
        self.timeframe = pygame.time.get_ticks()
        self.v = 10


    # I'd really love to do all this in Godot or something, but, well...
    # Hell, I can't even GPT my way through this mess!
    # Pygame is way too primitive for my (well not so much even mine anymore haha) idea.
    # I'm never signing up for something like this ever again.
    def update(self, fps, *args) -> None:
        if not any(self.dict_move.values()):
            if pygame.time.get_ticks() - self.timeframe > 600:
                self.cur_frames = (self.cur_frames + 1) % 2
                self.image = self.frames[self.cur_frames]
        else:
            if self.dict_move[pygame.K_s]:
                self.move(self.pos[0], self.pos[1] + self.v // fps)
                self.update_frames(0)
            if self.dict_move[pygame.K_w]:
                self.move(self.pos[0], self.pos[1] + self.v // fps)
                self.update_frames(1)
            if self.dict_move[pygame.K_a]:
                self.move(self.pos[0], self.pos[1] + self.v // fps)
                self.update_frames(2)
            if self.dict_move[pygame.K_d]:
                self.move(self.pos[0], self.pos[1] + self.v // fps)
                self.update_frames(3)

        if args and args[0].type == pygame.KEYDOWN:
            key = args[0].key
            if key in self.dict_move:
                self.dict_move[key] = True

        if args and args[0].type == pygame.KEYUP:
            key = args[0].key
            if key in self.dict_move:
                self.dict_move[key] = False

    def update_frames(self, start=0):
        if pygame.time.get_ticks() - self.timeframe > 500:
            self.cur_frames = Mireaman.row + (self.cur_frames + 1) % Mireaman.col
            self.timeframe = pygame.time.get_ticks()
        self.image = self.frames[self.cur_frames]
