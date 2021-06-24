import pygame
from  pygame.sprite import Sprite
from alien import Alien

class Bonus(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.img = pygame.image.load("alien_invasion/other_files/bonus.png")
        self.rect = self.img.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = float(ai_game.alien.y)
        self.x = ai_game.alien.rect.y

    def update(self):
        """Перемещает бонус вниз по экрану"""
        self.y += self.settings.bonus_speed
        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        """Рисует бонус в текущей позиции"""
        self.screen.blit(self.img, self.rect)