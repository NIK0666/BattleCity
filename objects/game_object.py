import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite


class GameObject(Sprite):
    """Класс отображаемых объектов"""
    rect: Rect = None
    image = None

    def __init__(self, screen, image_name=None):
        super(GameObject, self).__init__()
        self.screen = screen
        if image_name:
            self.image = pygame.image.load("res/" + image_name)
            self.rect = self.image.get_rect()

    def update(self):
        pass

    def render(self):
        if self.image and self.rect:
            self.screen.blit(self.image, self.rect)
