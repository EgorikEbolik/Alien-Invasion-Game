class GameStats():
    """Отслеживание статистики"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""

        self.settings = ai_game.settings
        self.reset_status()
        self.game_active = False
        self.read_high_score()

    def read_high_score(self):
        """Читает рекорд"""
        
        filename = 'record.txt'
        with open(filename) as f:
            self.high_score = f.read()

    def reset_status(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""

        self.ships_left = self.settings.ship_limit

        # Игра запускается в активном состоянии
        self.game_active = True
        self.score = 0
        self.level = 1