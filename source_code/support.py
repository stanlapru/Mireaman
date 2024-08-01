import pygame, os
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
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')  # List of supported image extensions

    for _, __, files in os.walk(path):
        for file in files:
            if file.lower().endswith(valid_extensions):  # Check if the file has a valid image extension
                full_path = os.path.join(path, file)
                try:
                    image_surface = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surface)
                except pygame.error as e:
                    print(f"Unable to load image {full_path}: {e}")
    return surface_list