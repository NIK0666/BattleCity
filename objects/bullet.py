import pygame

from objects.game_object import GameObject
from enums.control_enums import MoveDirection
from helpers.helper_classes import Pos


class Bullet(GameObject):

    def __init__(self, model, owner, controller):
        super(Bullet, self).__init__(controller.screen, model['Image'])
        self.owner = owner
        self.controller = controller

        if owner.see_direction == MoveDirection.UP:
            self.image = pygame.transform.rotate(self.image, 0)
            self.rect = self.image.get_rect()
            self.rect.centerx = owner.rect.centerx
            self.rect.top = owner.rect.top
            self.offset = 0, -float(model['Speed'])
        elif owner.see_direction == MoveDirection.DOWN:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect()
            self.rect.centerx = owner.rect.centerx
            self.rect.bottom = owner.rect.bottom
            self.offset = 0, float(model['Speed'])
        elif owner.see_direction == MoveDirection.LEFT:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.left = owner.rect.left
            self.rect.centery = owner.rect.centery
            self.offset = -float(model['Speed']), 0
        elif owner.see_direction == MoveDirection.RIGHT:
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
            self.rect.right = owner.rect.right
            self.rect.centery = owner.rect.centery
            self.offset = float(model['Speed']), 0

        self.pos = Pos(self.rect.x, self.rect.y)

    def update(self):
        # Обновляем позицию пули
        self.pos.x += self.offset[0] * self.controller.dt
        self.pos.y += self.offset[1] * self.controller.dt
        super(Bullet, self).update()

        # Проверяем коллизию
        # self.__check_collision()

    # def __check_collision(self):
    # surface = pygame.sprite.spritecollideany(self, self.controller.current_level.map)
    # if surface:
    #     # Обрабатываем столкновение с поверхностью
    #     # surface.hit(self)
    #     # Удаляем саму пулю
    #     self.controller.current_level.bullets.remove(self)
