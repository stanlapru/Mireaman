import pygame
from csv import reader
from os import walk


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path):
    surface_list = []
    for _,__,files in walk(path):
        for image in files:
            full_path = path + '/' + image
            if full_path[-4:] == '.png':
                image_surface = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surface)
    return surface_list