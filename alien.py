import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        """Инициализация пришельца и установка начальной позиции"""

        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('alien_invasion/other_files/ufo.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.settings = ai_game.settings
    def update(self):
        """Перемещает пришельца влево или вправо"""

        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Возвращяет True, если достигнут край  экрана"""

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True