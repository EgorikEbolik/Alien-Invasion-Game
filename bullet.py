import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс снарядов корабля"""

    def __init__(self, ai_game):
        """Создаёт объект снарядов в текущей позиции корабля"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # создание снаряда в позиции (0, 0) и назначение правильной позиции
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""

        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)