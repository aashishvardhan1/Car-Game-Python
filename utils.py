import pygame


def scale_image(img, factor):
    size = round(img.get_width() * factor * 0.8), round(img.get_height() * factor * 0.8)
    return pygame.transform.scale(img, size)