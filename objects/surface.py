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

    # def hit(self, bullet):
    #     # Проверим разрушаемость
    #     if self.is_destructible:
    #         # Если еще не разбили на части то разобьем
    #         if self.health == 4:
    #             c1 = pygame.image.load("res/" + self.model['Image_01'])
    #             c2 = pygame.image.load("res/" + self.model['Image_02'])
    #             c3 = pygame.image.load("res/" + self.model['Image_03'])
    #             c4 = pygame.image.load("res/" + self.model['Image_04'])
    #             self.cells = {
    #                 c1: pygame.rect.Rect(self.rect.x + 0, self.rect.y + 0, 32, 32),
    #                 c2: pygame.rect.Rect(self.rect.x + 32, self.rect.y + 0, 32, 32),
    #                 c3: pygame.rect.Rect(self.rect.x + 0, self.rect.y + 32, 32, 32),
    #                 c4: pygame.rect.Rect(self.rect.x + 32, self.rect.y + 32, 32, 32)
    #             }
    #
    #         # Проверим на столкновение с кусочком
    #         for img in self.cells.copy():
    #             if self.cells[img].colliderect(bullet.rect):
    #                 del self.cells[img]
    #                 self.health -= 1
