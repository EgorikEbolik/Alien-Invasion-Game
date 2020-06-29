import pygame.font
from pygame.sprite import Group

from ship import Ship


class ScoreBoard():
    """Выводит Информацию о игре"""

    def __init__(self, ai_game):
        """Инициализация атрибутов подсчёта очков"""

        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройка шрифта
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(
            'alien_invasion/other_files/pixel.ttf', 48)
        # Подготовка исходнодного изображения счётов
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует счёт в картинку"""

        rounded_score = round(self.stats.score, -1)

        score_str = "Score:{:,}".format(rounded_score)
        self.score_img = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Вывод счёта в правом верхнем углу
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Преобразует рекордный счёт в изображение"""

        high_score = self.stats.high_score
        high_score_str = f"Record:{high_score}"
        self.high_score_img = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Преобразует уровень в изображение"""
        level = self.stats.level
        level_str = f"LVL:{level}"
        self.level_img = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        # Уровень выводится под текущим счётом
        self.level_rect = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """Вывод счёта на экран"""

        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд"""

        self.stats.high_score = int(self.stats.high_score)
        
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def write_high_score(self):
        """Записыает наибольший рекорд в файл"""

        self.stats.high_score = int(self.stats.high_score)
        
        if self.stats.score >= self.stats.high_score:
            self.stats.high_score = self.stats.score

            filename = 'record.txt'
            with open(filename, "w") as f:
                f.write(str(self.stats.high_score))

    def read_high_score(self):
        """Читает рекорд"""

        filename = 'record.txt'
        with open(filename) as f:
            self.high_score = f.read()

    def prep_ships(self):
        """Показывает количество оставшихся кораблей"""

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.image.load(
                'alien_invasion/other_files/spaceship_small.png')
            ship.rect.x = 10 + ship_number * ship.rect.width / 2
            ship.rect.y = 10
            self.ships.add(ship)
