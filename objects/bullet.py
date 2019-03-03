import pygame

from pygame.sprite import Sprite
from enums.control_enums import MoveDirection


class Bullet(Sprite):

    def __init__(self, model, owner, controller):
        super(Bullet, self).__init__()
        self.owner = owner
        self.controller = controller
        self.level = self.controller.current_level
        path = "res/" + model['Image']

        if owner.see_direction == MoveDirection.UP:
            self.image = pygame.transform.rotate(pygame.image.load(path), 0)
            self.rect = self.image.get_rect()
            self.rect.centerx = owner.rect.centerx
            self.rect.top = owner.rect.top
            self.offset = 0, -float(model['Speed'])
        elif owner.see_direction == MoveDirection.DOWN:
            self.image = pygame.transform.rotate(pygame.image.load(path), 180)
            self.rect = self.image.get_rect()
            self.rect.centerx = owner.rect.centerx
            self.rect.bottom = owner.rect.bottom
            self.offset = 0, float(model['Speed'])
        elif owner.see_direction == MoveDirection.LEFT:
            self.image = pygame.transform.rotate(pygame.image.load(path), 90)
            self.rect = self.image.get_rect()
            self.rect.left = owner.rect.left
            self.rect.centery = owner.rect.centery
            self.offset = -float(model['Speed']), 0
        elif owner.see_direction == MoveDirection.RIGHT:
            self.image = pygame.transform.rotate(pygame.image.load(path), -90)
            self.rect = self.image.get_rect()
            self.rect.right = owner.rect.right
            self.rect.centery = owner.rect.centery
            self.offset = float(model['Speed']), 0

        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)
        self.level.bullets.add(self)

    def update(self):
        # Обновляем позицию пули
        self.pos_x += self.offset[0] * self.controller.dt
        self.pos_y += self.offset[1] * self.controller.dt
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        # Проверяем коллизию
        # self.__check_collision()

    def render(self):
        self.level.screen.blit(self.image, self.rect)

    # def __check_collision(self):
        # surface = pygame.sprite.spritecollideany(self, self.controller.current_level.map)
        # if surface:
        #     # Обрабатываем столкновение с поверхностью
        #     # surface.hit(self)
        #     # Удаляем саму пулю
        #     self.controller.current_level.bullets.remove(self)

