import pygame

from pygame.sprite import Sprite
from pygame.sprite import Group
from objects.surface import Surface
from objects.spawn_anim import SpawnAnimation


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
        for bullet in self.bullets.sprites():
            bullet.update()
        self.controller.player.update()

        self.__check_collisions()

    def render(self):
        for animation in self.animations.sprites():
            animation.render()

        for surface in self.map_back.sprites():
            surface.render()

        for bullet in self.bullets.sprites():
            bullet.render()

        self.controller.player.render()

        for surface in self.map.sprites():
            surface.render()

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
                    self.player_spawn = self.__get_point(row, col)
                    self.controller.player.set_pos(self.player_spawn[0], self.player_spawn[1])
                # Точка спавна врагов
                elif surface_type == "s":
                    pt = self.__get_point(row, col)
                    self.enemy_spawn_points.append(self.__get_point(row, col))

                    spawn_animation = SpawnAnimation(self.screen)
                    spawn_animation.pt = pt
                    self.animations.add(spawn_animation)
                # Строим карту
                elif not surface_type == "0":
                    self.__create_surface(surface_type, row, col)

    def __create_surface(self, surface_type, row, col):
        surface = Surface(self.__get_surface_model(surface_type), self.screen)
        pt = self.__get_point(row, col)
        surface.rect.x = pt[0]
        surface.rect.y = pt[1]
        if surface.is_blocks_movement:
            self.map.add(surface)
        else:
            self.map_back.add(surface)

    def __check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.map, True, False)
        if collisions:
            for bullet, surfaces in collisions.items():
                for surface in surfaces:
                    if surface.is_destructible:
                        self.map.remove(surface)

    @classmethod
    def __get_point(cls, row, col):
        return 64 * col, 64 * row

    def __get_surface_model(self, surface_type):
        return self.surfaces_config[self.surfaces_config['DEFAULT'][surface_type]]
