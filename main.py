import pygame
import configparser

from controllers.game_controller import GameController


def run_game():
    """Инициализируем игру"""
    pygame.init()

    # Считываем конфиг
    config = configparser.ConfigParser()
    config.read("configs/config.ini")

    # Настройка окна
    width = int(config['WINDOW']['Width'])
    height = int(config['WINDOW']['Height'])
    title = config['WINDOW']['Title']
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    GameController(screen, config)


if __name__ == "__main__":
    run_game()
