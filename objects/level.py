import pygame

from pygame.sprite import Sprite
from pygame.sprite import Group
from pygame.rect import Rect
from objects.surface import Surface
from objects.surface import SurfaceCell
from objects.spawn_anim import SpawnAnimation
import helpers.helper_functions as helpers


class Level(Sprite):
    """Класс уровня"""

    def __init__(self, config, controller):
        super(Level, self).__init__()
        self.config = config
        self.surfaces_config = controller.surfaces_config
        self.controller = controller
        self.screen = self.controller.screen
        self.caption = config["MAP"]["Caption"]
        self.map = Group()
        self.map_back = Group()
        self.animations = Group()
        self.bullets = Group()
        self.grid = []
        self.player_spawn = (0, 0)
        self.enemy_spawn_points = []

        self.__build_map()

    def update(self):
        """Обновление состояний объектов уровня"""
        for bullet in self.bullets.sprites():
            bullet.update()
        self.controller.player.update()

    def render(self):
        """Отрисовка уровня"""
        for animation in self.animations.sprites():
            animation.render()

        for surface in self.map_back.sprites():
            surface.render()

        for surface in self.map.sprites():
            surface.render()

        for bullet in self.bullets.sprites():
            bullet.render()

        self.controller.player.render()

    def destruct_cell(self, surface, bullet):
        self.map.remove(surface)
        if surface.health == 4:
            # делим на 4 штуки

            if not helpers.intersects(Rect(surface.rect.x, surface.rect.y, 32, 32), bullet.rect):
                self.__create_surface_cell(surface.model, surface.rect.y // 64, surface.rect.x // 64, 0, 0)
            if not helpers.intersects(Rect(surface.rect.x, surface.rect.y + 32, 32, 32), bullet.rect):
                self.__create_surface_cell(surface.model, surface.rect.y // 64, surface.rect.x // 64, 0, 1)
            if not helpers.intersects(Rect(surface.rect.x + 32, surface.rect.y, 32, 32), bullet.rect):
                self.__create_surface_cell(surface.model, surface.rect.y // 64, surface.rect.x // 64, 1, 0)
            if not helpers.intersects(Rect(surface.rect.x + 32, surface.rect.y + 32, 32, 32), bullet.rect):
                self.__create_surface_cell(surface.model, surface.rect.y // 64, surface.rect.x // 64, 1, 1)

        self.bullets.remove(bullet)

    def __build_map(self):
        """Создание карты на основе конфига"""
        # Распарсим из конфига в двумерный массив
        temp = self.config["MAP"]["Grid"].split('\n')
        for val in temp:
            self.grid.append(val.split(','))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                surface_type = self.grid[row][col]
                # Точка спавна игрока
                if surface_type == "p":
                    self.player_spawn = helpers.get_point(row, col)
                    self.controller.player.set_pos(self.player_spawn[0], self.player_spawn[1])
                # Точка спавна врагов
                elif surface_type == "s":
                    pt = helpers.get_point(row, col)
                    self.enemy_spawn_points.append(helpers.get_point(row, col))

                    spawn_animation = SpawnAnimation(self.screen)
                    spawn_animation.pt = pt
                    self.animations.add(spawn_animation)
                # Строим карту
                elif not surface_type == "0":
                    self.__create_surface(surface_type, row, col)

    def __create_surface(self, surface_type, row, col):
        """Создание 'клетки' карты"""
        surface = Surface(self.__get_surface_model(surface_type), self.screen)
        pt = helpers.get_point(row, col)
        surface.rect.x = pt[0]
        surface.rect.y = pt[1]
        if surface.is_blocks_movement:
            self.map.add(surface)
        else:
            self.map_back.add(surface)

    def __create_surface_cell(self, surface_model, row, col, subrow, subcol):
        """Создание маленькой 'клетки' карты"""
        surface = SurfaceCell(surface_model, self.screen, subrow * 1 + subcol * 2 + 1)
        pt = helpers.get_point(row, col, subrow, subcol)
        surface.rect.x = pt[0]
        surface.rect.y = pt[1]
        if surface.is_blocks_movement:
            self.map.add(surface)
        else:
            self.map_back.add(surface)

    def __get_surface_model(self, surface_type):
        """Получение данных о типе поверхности"""
        return self.surfaces_config[self.surfaces_config['DEFAULT'][surface_type]]
