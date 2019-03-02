import pygame

from pygame.sprite import Sprite
from enums.control_enums import MoveDirection


class Bullet(Sprite):

    def __init__(self, owner, level):
        super(Bullet, self).__init__()
        self.owner = owner
        self.level = level



