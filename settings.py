class Settings():
    """В этом классе все настройки"""

    def __init__(self):

        # параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 19, 50)

        # Настройки коробля
        self.ship_limit = 3

        # параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullet_allowed = 3

        # Ускорение игры
        self.speedup_scale = 1.1

        # Настройка прищельцев
        self.fleet_drop_speed = 10

        # self.fleet_direction 1 - движение вправо. self.fleet_direction -1 -движение влево
        self.fleet_direction = 1

        #Темп роста стоимости пришельцев
        self.score_scale = 1.5
    def dynamic_settings(self):
        self.alien_speed = 1.0
        self.bullet_speed = 1.5
        self.ship_speed = 1.5
        # Подсчёт очков
        self.alien_points = 10  

    def inscrease_speed(self):
        """Увеличивает настройки скорости"""

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)