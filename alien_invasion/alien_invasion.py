import sys
from random import randint, randrange
import pygame
from pygame import Rect
from time import sleep
import os

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Star
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from bonus import Bonus

class AlienInvasion:

    def __init__(self):

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = ScoreBoard(self) 

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.alien = Alien(self)
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.stars = pygame.sprite.Group()
        self._create_stars_grid()

        self.bonus = pygame.sprite.Group()
        
        self.easy_button = Button(self, 850, 250, (102, 255, 0), "Easy")
        self.normal_button = Button(self, 850, 450, (255, 216, 0), "Normal")
        self.hard_button = Button(self, 850, 650, (255, 36, 0), "Hard")
        self.zerout_record_button = Button( 
            self, 850, 850, (0, 0, 0), "Zero out a record")

    def run_game(self):
        """Запускает основной цикл игры"""

        while True:
            self._check_events()
            self.sb.read_high_score()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_bonus()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает события клавиш и мыши"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._difficulty_buttons(mouse_pos)
                self._check_play_button(mouse_pos)
                self._zerout_record(mouse_pos)

    def _check_keydown_events(self, event):
        """Реакция на нажите клавиш"""

        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            self.sb.write_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реакция на отпускание клавиш"""

        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _zerout_record(self, mouse_pos):
        """Обнуляет рекорд при нажатии кнопки"""

        button_clicked = self.zerout_record_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            os.system('python D:\\Programming\\Python\\alien_invasion\\start.py')
            sys.exit()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки play"""

        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked or normal_button_clicked or hard_button_clicked and not self.stats.game_active:
            # Cброс статистики
            self.stats.reset_status()
            self.stats.game_active = True
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked or normal_button_clicked or hard_button_clicked and not self.stats.game_active:
            pygame.mixer.music.load(
                'PY/alien_invasion/other_files/for_levels.mp3')
            pygame.mixer.music.set_volume(50)
            pygame.mixer.music.play(-1)
            if easy_button_clicked:
                self.settings.dynamic_settings()
                self.settings.alien_speed = 0.7
                self.settings.ship_speed = 1.8
                self.settings.bullet_speed = 1.9
                self._check_play_button(mouse_pos)
            if normal_button_clicked: 
                self.settings.dynamic_settings()
                self.settings.alien_speed = 1.0
                self.settings.ship_speed = 1.5
                self.settings.bullet_speed = 1.5
                self._check_play_button(mouse_pos)
            if hard_button_clicked:
                self.settings.dynamic_settings()
                self.settings.alien_speed = 1.8
                self.settings.ship_speed = 0.8
                self.settings.bullet_speed = 0.7
                self._check_play_button(mouse_pos)


    def _bonus_start_fly(self):
        """Создание нового бонуса и добавление в группу"""
        
        if len(self.bonus) < self.settings.bonus_allowed and randint(0, 75) > 70 :
            new_bonus = Bonus(self)
            self.bonus.add(new_bonus)

    def _update_bonus(self):
        """Обновляет места бонусов и убирает старые бонусы"""
        
        self.bonus.update()
        
        for new_bonus in self.bonus.copy():
            if new_bonus.rect.bottom <= 1080:
                self.bullets.remove(new_bonus)
        self._check_bullet_alien_collisions()

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу"""

        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            fire_sound = pygame.mixer.Sound("PY/alien_invasion/other_files/shot.wav")
            fire_sound.play()

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.bonus.empty()
            self.settings.inscrease_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()
        # проверка попаданий в пришельцев.При попадании удаляет снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            #self._bonus_start_fly()
            hit_sound = pygame.mixer.Sound(
                'PY/alien_invasion/other_files/ufo.wav')
            hit_sound.play()

            self.sb.prep_score()
            self.sb.check_high_score()

    def _create_fleet(self):
        """Создание флота пришельцев"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaible_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaible_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране"""

        ship_height = self.ship.rect.height
        avaible_space_y = (self.settings.screen_height -
                           (3 * alien_height) - ship_height)
        number_rows = avaible_space_y // (2 * alien_height)

        # Создание флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реакция на достижение края экрана"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self): 
        """Опускает флот и меняет направление"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_aliens(self):
        """Обновляет позиции всех прищельцев"""

        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий пришельца с кораблём
        if pygame.sprite.spritecollide(self.ship, self.aliens, True):
            self._ship_hit()

        # Проверяет, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _create_stars_grid(self):
        """Создание сетки звёзд"""

        # Создание одной звезды
        star = Star(self)

        avaible_star_space_x = self.settings.screen_width
        avaible_star_space_y = self.settings.screen_height

        star_height = star.rect.y
        star_width = star.rect.x

        i = 0

        star_x = [0]
        star_y = [0]
        for i in range(60):
            cur_pos_x = randrange(0, 1900, 50)
            cur_pos_y = randrange(0, 1080, 45)
            for x in star_x:
                if cur_pos_x == x:
                    cur_pos_x = randrange(0, 1900, 50)
                    star_x.append(cur_pos_x)
                    break
                else:
                    star_x.append(cur_pos_x)
                    break

            for y in star_y:
                if cur_pos_y == y:
                    cur_pos_y = randrange(0, 1080, 45)
                    star_y.append(cur_pos_y)
                    break
                else:
                    star_y.append(cur_pos_y)
                    break
            if star_x[i] == 0 and star_y[i] == 0:
                star.remove()

            else:
                self._create_star(star_x[i], star_y[i])

    def _create_star(self, x, y):
        star = Star(self)

        star.rect.x = x
        star.rect.y = y

        self.stars.add(star)

    def _ship_hit(self):
        """Обрабатывает столкновения корабля с пришельцами"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left
            self.stats.ships_left -= 1
            
            #Проигравание звука при потере жизни
            ship_hit_sound = pygame.mixer.Sound('alien_invasion/other_files/minus_hp.wav')
            ship_hit_sound.play()
            
            self.sb.prep_ships()

            # Очистка списков пришельцев и пуль
            self.aliens.empty()
            self.bullets.empty()

            # Созание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Обновляет изображение на экране"""
        self.screen.fill(self.settings.bg_color)

        self.stars.draw(self.screen)
        self.sb.show_score()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        for bonus in self.bonus.sprites():
            bonus.blitme()

        if not self.stats.game_active:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.zerout_record_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
