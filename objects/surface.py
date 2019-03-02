import pygame

from pygame.sprite import Sprite


class Surface(Sprite):
    """Класс клетки карты"""

    def __init__(self, model, screen):
        super(Surface, self).__init__()
        self.screen = screen
        self.rect = pygame.rect.Rect(0, 0, 64, 64)

        # Загрузка изображения пришельца и назначение атрибута rect
        self.image = pygame.image.load("res/" + model['Image'])
        self.rect = self.image.get_rect()
        self.is_blocks_movement = model['BlocksMovement'] == "True"

    def render(self):
        """Выводит ячейку карты в текущем положении"""
        self.screen.blit(self.image, self.rect)
