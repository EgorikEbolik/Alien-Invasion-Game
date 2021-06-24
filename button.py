import pygame.font


class Button():
    def __init__(self, ai_game, x, y, color, msg):
        """Инициализирует атрибуты кнопки"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопок
        self.width, self.height = 200, 84
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(
            'other_files/pixel.ttf', 48)

        # Построение объекта rect и выравнивание по центру
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.screen_rect.x = x
        self.screen_rect.y = y

        self.rect.x = self.screen_rect.x

        self.rect.y = self.screen_rect.y

        # Сообщение кнопки создаётся только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""

        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Отображение пустой кнопки и вывод сообщения"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
