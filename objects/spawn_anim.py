import pyganim
import pygame
from pygame.sprite import Sprite


class SpawnAnimation(Sprite):

    def __init__(self, screen):
        super(SpawnAnimation, self).__init__()
        self.screen = screen
        images = pyganim.getImagesFromSpriteSheet('res/spawn_anim.bmp',rects=[
            (0, 0, 64, 64), (64, 0, 64, 64), (128, 0, 64, 64),
            (192, 0, 64, 64), (256, 0, 64, 64), (320, 0, 64, 64),
            (384, 0, 64, 64), (448, 0, 64, 64), (512, 0, 64, 64),
            (0, 64, 64, 64), (64, 64, 64, 64), (128, 64, 64, 64),
            (192, 64, 64, 64), (256, 64, 64, 64), (320, 64, 64, 64),
            (384, 64, 64, 64), (448, 64, 64, 64), (512, 64, 64, 64)])
        frames = list(zip(images, [64] * len(images)))
        self.animationObj = pyganim.PygAnimation(frames)
        self.animationObj.play()
        self.pt = (0, 0)

    def render(self):
        self.animationObj.blit(self.screen, self.pt)
