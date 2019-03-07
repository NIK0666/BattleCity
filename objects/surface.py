import pygame

from objects.game_object import GameObject


class Surface(GameObject):
    """Класс клетки карты"""

    def __init__(self, model, screen):
        super(Surface, self).__init__(screen, model['Image'])
        self.screen = screen
        self.rect = pygame.rect.Rect(0, 0, 64, 64)
        self.model = model

        self.is_blocks_movement = model['BlocksMovement'] == "True"
        self.is_blocks_bullets = model['BlocksBullets'] == "True"
        self.is_destructible = model['Destructible'] == "True"
        if self.is_destructible:
            self.health = 4


class SurfaceCell(GameObject):

    def __init__(self, model, screen, index):
        super(SurfaceCell, self).__init__(screen, model['Image_0' + str(index)])
        self.screen = screen
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.model = model

        self.is_blocks_movement = model['BlocksMovement'] == "True"
        self.is_blocks_bullets = model['BlocksBullets'] == "True"
        self.is_destructible = model['Destructible'] == "True"
        if self.is_destructible:
            self.health = 1
