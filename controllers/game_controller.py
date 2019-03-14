import pygame
import sys
import configparser

from objects.tank import Tank
from objects.level import Level
from enums.control_enums import MoveDirection
from objects.bullet import Bullet
from controllers.ai_controller import AIController


class GameController:
    """Отвечает за управление игрой"""

    def __init__(self, screen, config):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Время с момента последнего вызова
        self.clock = pygame.time.Clock()
        self.dt = 0

        # Получаем конфиг поверхностей
        self.surfaces_config = configparser.ConfigParser()
        self.surfaces_config.read("configs/surfaces.ini")

        # Получаем конфиг пуль
        self.bullets_config = configparser.ConfigParser()
        self.bullets_config.read("configs/bullets.ini")

        # Создаем танк игрока
        self.tanks_config = configparser.ConfigParser()
        self.tanks_config.read("configs/tanks.ini")
        print(config['DEFAULT']['PlayerTank'])
        self.player = Tank(self, self.tanks_config[config['DEFAULT']['PlayerTank']])

        # Распарсим с конфига доступные уровни
        self.levels = config['DEFAULT']['Levels'].split(',')

        # Создаем уровень
        level_config = configparser.ConfigParser()
        level_config.read("configs/" + self.levels[0] + ".ini")
        self.current_level = Level(level_config, self)

        self.ai_controller = AIController()

        # Запускаем цикл обновления
        self.__game_loop()

    def create_bullet(self, tank, model):
        bullet = Bullet(model, tank, self)
        self.current_level.bullets.add(bullet)

    def __game_loop(self):
        while True:
            self.dt = self.clock.tick(60)
            self.__check_events()
            self.__update_screen()

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            self.__check_control(event)

    def __update_screen(self):
        self.screen.fill((0, 0, 0))
        self.current_level.update()
        self.__check_collisions()
        self.current_level.render()
        pygame.display.flip()

    def __check_collisions(self):
        """Проверка коллизий"""
        # Проверяем столкновение пули с поверхностями карты
        collisions = pygame.sprite.groupcollide(self.current_level.bullets, self.current_level.map, False, False)
        if collisions:
            for bullet, surfaces in collisions.items():
                for surface in surfaces:
                    if surface.is_blocks_bullets:
                        if surface.is_destructible:
                            self.current_level.destruct_cell(surface, bullet)
                        else:
                            self.current_level.bullets.remove(bullet)

        # Проверяем столкновение игрока с поверхностями карты
        collisions = pygame.sprite.spritecollideany(self.player, self.current_level.map)
        if collisions:
            if self.player.direction == MoveDirection.UP:
                self.player.rect.top = collisions.rect.bottom
            elif self.player.direction == MoveDirection.DOWN:
                self.player.rect.bottom = collisions.rect.top
            elif self.player.direction == MoveDirection.LEFT:
                self.player.rect.left = collisions.rect.right
            elif self.player.direction == MoveDirection.RIGHT:
                self.player.rect.right = collisions.rect.left
            self.player.pos.x = float(self.player.rect.x)
            self.player.pos.y = float(self.player.rect.y)

    def __check_control(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.player.move(MoveDirection.UP)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.player.move(MoveDirection.DOWN)
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.player.move(MoveDirection.RIGHT)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.player.move(MoveDirection.LEFT)
            if event.key == pygame.K_SPACE:
                self.player.fire()

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.player.direction == MoveDirection.UP:
                self.player.move(MoveDirection.NONE)
            if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.player.direction == MoveDirection.DOWN:
                self.player.move(MoveDirection.NONE)
            if (
                    event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.player.direction == MoveDirection.RIGHT:
                self.player.move(MoveDirection.NONE)
            if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.player.direction == MoveDirection.LEFT:
                self.player.move(MoveDirection.NONE)
