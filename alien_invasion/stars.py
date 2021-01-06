import pygame
from pygame.sprite import  Sprite

class Star(Sprite):
    """Класс звезды"""
    
    def __init__(self, ai_game):
        """Инизиализирует звёзды"""
        
        super().__init__()
        self.screen = ai_game.screen
        
        self.image = pygame.image.load('PY/alien_invasion/other_files/star.png')
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)