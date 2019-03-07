import pygame

from objects.game_object import GameObject
from enums.control_enums import MoveDirection
from objects.bullet import Bullet


class Tank(GameObject):
    """Класс танка"""

    def __init__(self, controller, config):
        """Конфигурация танка находится в конфиг файле, тут только логика"""
        super(Tank, self).__init__(controller.screen, config['DEFAULT']['Image'])
        self.controller = controller
        self.bullet_model = controller.bullets_config[config['DEFAULT']['Bullet']]

        # Загрузка изображения танка и назначение атрибута rect
        self.original_image = self.image.copy()

        # Начальная координата танка
        self.rect.x = 0
        self.rect.y = 0

        # Позиция с дробными значениями
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

        # Скорость танка
        self.speed = float(config['DEFAULT']['Speed'])

        # По умолчанию танк не движется
        self.direction = MoveDirection.NONE
        self.see_direction = MoveDirection.UP

    def set_pos(self, _x, _y):
        """Задает позицию танка на уровне"""
        # Начальная координата танка
        self.rect.x = _x
        self.rect.y = _y

        # Позиция с дробными значениями
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)

    def move(self, direction):
        """Смещает танк в заданном направлении"""
        if not direction == MoveDirection.NONE:
            self.see_direction = direction
        self.direction = direction

        if not direction == MoveDirection.NONE:
            # Скорректируем позицию

            if direction == MoveDirection.LEFT or direction == MoveDirection.RIGHT:
                # Поправим Y координату
                self.pos_y = 32 * round(self.pos_y / 32)
            else:
                # Поправим X координату
                self.pos_x = 32 * round(self.pos_x / 32)

            # Повернем текстуру относительно выбранного направления
            choice = {
                MoveDirection.LEFT: 90,
                MoveDirection.RIGHT: -90,
                MoveDirection.UP: 0,
                MoveDirection.DOWN: 180
            }
            angle = choice.get(self.direction, (0, 0))
            self.image = pygame.transform.rotate(self.original_image, angle)

    def fire(self):
        """Производит выстрел в сторону направления танка"""
        Bullet(self.bullet_model, self, self.controller)

    def update(self):
        """Обновляет позицию, вызывает проверку коллизий"""
        offset = {
            MoveDirection.LEFT: (-self.speed, 0),
            MoveDirection.RIGHT: (self.speed, 0),
            MoveDirection.UP: (0, -self.speed),
            MoveDirection.DOWN: (0, self.speed)
        }
        (_x, _y) = offset.get(self.direction, (0, 0))
        self.pos_x += _x * self.controller.dt
        self.pos_y += _y * self.controller.dt

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        self.__check_collision()

    def __check_collision(self):
        collisions = pygame.sprite.spritecollideany(self, self.controller.current_level.map)
        if collisions:
            if self.direction == MoveDirection.UP:
                self.pos_y = collisions.rect.y + collisions.rect.height
            elif self.direction == MoveDirection.DOWN:
                self.pos_y = collisions.rect.y - collisions.rect.height
            elif self.direction == MoveDirection.LEFT:
                self.pos_x = collisions.rect.x + collisions.rect.width
            elif self.direction == MoveDirection.RIGHT:
                self.pos_x = collisions.rect.x - collisions.rect.width
            self.rect.x = int(self.pos_x)
            self.rect.y = int(self.pos_y)
