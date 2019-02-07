import pygame
import os

_image_library = {}


def get_image(path, alpha=True):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        normalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        if alpha: image = pygame.image.load(normalized_path).convert_alpha()
        else: image = pygame.image.load(normalized_path).convert()
        _image_library[path] = image
    return image
