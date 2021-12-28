import random
import pygame

# Globals and initialization
from project.pygame_globals import PygameGlobals
from project.cars import Player, Enemy, TimeBooster, SpeedBooster
from project.widgets import Widget

import time
import json
import os
from pathlib import Path
from typing import List

current_globals = PygameGlobals()


def get_car_image(car_image):
    return pygame.image.load(os.path.join(PygameGlobals.MEDIA_DIR, car_image))


def quit_game():
    with open(os.path.join(PygameGlobals.BASE_DIR, "data.txt"), "w", encoding="utf-8") as output:
        for score in PygameGlobals.SCORES:
            output.write(f"{score}\n")

    with open(
            os.path.join(
                PygameGlobals.BASE_DIR,
                "settings.txt"
            ), "w", encoding="utf-8"
    ) as settings_write:
        settings_write.write(json.dumps(PygameGlobals.all_settings, indent=4))
    exit()


def buy_car(number):
    if PygameGlobals.all_settings['player_money'] < (number + 1) * 100:
        notification = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
            18
        )
        notification_surface = notification.render(
            'Not enough money',
            True,
            (255, 255, 255)
        )
        PygameGlobals.screen.blit(notification_surface, (0, 0))
        return
    if number in PygameGlobals.all_settings['cars_bought']:
        return
    PygameGlobals.all_settings['player_money'] -= number * 100
    PygameGlobals.all_settings['player_car'] = f'car{number}.png'
    PygameGlobals.all_settings['player_speed'] = 15 + 2 * (number - 1)
    PygameGlobals.all_settings['cars_bought'].append(number)
    bought_notification = pygame.font.Font(
        os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
        18
    )
    bought_notification_surface = bought_notification.render(
        f'Bought car {number}',
        True, (255, 255, 255)
    )
    PygameGlobals.screen.blit(bought_notification_surface, (0, 0))


def use_car(number):
    if number not in PygameGlobals.all_settings['cars_bought']:
        car_not_bought_notification = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
            18
        )
        car_not_bought_notification_surface = car_not_bought_notification.render(
            f'You did not buy car {number}',
            True,
            (255, 255, 255)
        )
        PygameGlobals.screen.blit(car_not_bought_notification_surface, (0, 0))
        return
    PygameGlobals.all_settings['player_car'] = f'car{number}.png'
    PygameGlobals.all_settings['player_speed'] = 15 + 2 * (number - 1)


def enemy_factory():
    image_path = PygameGlobals.CARS[random.randint(0, 7)]
    return Enemy(
        image_path,
        random.randint(
            PygameGlobals.width // 10,
            PygameGlobals.width - PygameGlobals.width // 3 - PygameGlobals.width // 9 - 30
        ),
        -100
    )


def booster_factory(string):
    kwargs = {'x': random.randint(
        PygameGlobals.width // 10, PygameGlobals.width - PygameGlobals.width // 3 - PygameGlobals.width // 9 - 30),
        'y': -100}

    if string == 'TimeBooster':
        kwargs['image_path'] = 'clock.png'
        return TimeBooster(**kwargs)
    elif string == 'SpeedBooster':
        kwargs['image_path'] = 'speed.png'
        return SpeedBooster(**kwargs)


class GameState:
    def __init__(self):
        self.state = 'menu'

    def main_game(self):
        prev_time = time.time()
        normal_prev_time = time.time()
        prev_booster_time = time.time()
        boost_time = None
        speed_boost_time = None
        time_boosted = False
        # Sprites

        # Player
        player_speed = PygameGlobals.all_settings['player_speed']
        player = Player(PygameGlobals.all_settings['player_car'])
        players = pygame.sprite.Group()
        players.add(player)

        # Boosters
        time_boosters = pygame.sprite.Group()
        speed_boosters = pygame.sprite.Group()

        # Enemy
        enemies = pygame.sprite.Group()
        enemy_speed = 30
        # Score

        score_number = 0
        speed_number = 120
        score = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
            25)
        current_car_speed = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, "FiraCodeBold.ttf"),
            25)
        score_surf = score.render(str(score_number), True, (255, 255, 255))
        current_car_speed_surf = current_car_speed.render(
            f"{speed_number} km/h", True, (255, 255, 255))

        y = 0
        background_speed = 20
        slow_down = False
        while True:
            rel_y = y % (PygameGlobals.height * 2)

            PygameGlobals.screen.fill((0, 0, 0))
            PygameGlobals.screen.blit(PygameGlobals.background_image, (0, rel_y))
            PygameGlobals.screen.blit(PygameGlobals.mountains, (PygameGlobals.width - PygameGlobals.width // 3, rel_y))
            if rel_y >= 0:
                PygameGlobals.screen.blit(PygameGlobals.background_image, (0, rel_y - PygameGlobals.height * 2))
                PygameGlobals.screen.blit(
                    PygameGlobals.mountains,
                    (PygameGlobals.width - PygameGlobals.width // 3, rel_y - PygameGlobals.height * 2))
            PygameGlobals.screen.blit(score_surf, (0, 0))
            PygameGlobals.screen.blit(current_car_speed_surf,
                                      (PygameGlobals.width - PygameGlobals.width // 3 - PygameGlobals.width // 6, 0))
            y += background_speed

            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    PygameGlobals.SCORES.append(score_number)
                    quit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.ride(-player_speed, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.ride(player_speed, 0)
                    elif event.key == pygame.K_UP:
                        player.ride(0, -player_speed)
                    elif event.key == pygame.K_DOWN:
                        player.ride(0, player_speed)
                if event.type == pygame.KEYUP:
                    player.stop()

            time_lapse = 0.5
            if time_boosted:
                time_lapse = 6

            if current_time - normal_prev_time >= 0.5:
                score_number += 1
                normal_prev_time = current_time
            score_surf = score.render(
                str(score_number),
                True,
                (255, 255, 255)
            )

            if current_time - prev_time >= time_lapse:
                prev_time = current_time
                enemy = enemy_factory()

                enemies.add(enemy)
                speed_number = round(speed_number + 0.1, 2)
                background_speed += 0.1
                enemy_speed += 0.1
                current_car_speed_surf = current_car_speed.render(
                    f"{speed_number} km/h",
                    True,
                    (255, 255, 255)
                )
            if current_time - (random.randint(20, 30) * time_lapse) >= prev_booster_time:
                random_booster_class = random.choice(
                    ['SpeedBooster', 'TimeBooster'])
                random_booster = booster_factory(
                    random_booster_class)
                if random_booster_class == 'SpeedBooster':
                    speed_boosters.add(random_booster)
                elif random_booster_class == 'TimeBooster':
                    time_boosters.add(random_booster)

                prev_booster_time = time.time()

            players.draw(PygameGlobals.screen)
            players.update()

            enemies.draw(PygameGlobals.screen)

            time_boosters.draw(PygameGlobals.screen)
            time_boosters.update(enemy_speed)

            speed_boosters.draw(PygameGlobals.screen)
            speed_boosters.update(enemy_speed)

            enemies.update(enemy_speed)
            collision_die = pygame.sprite.groupcollide(
                enemies, players, True, True)
            collision_time_boost = pygame.sprite.groupcollide(
                time_boosters, players, True, False
            )
            collision_speed_boost = pygame.sprite.groupcollide(
                speed_boosters, players, True, False
            )

            if collision_die:
                PygameGlobals.SCORES.append(score_number)
                PygameGlobals.all_settings['player_money'] += score_number
                self.state = 'game_over'

            pygame.display.flip()

            if collision_time_boost:
                current_globals.fps = 5
                boost_time = time.time()
                time_boosted = True
            elif boost_time is not None and current_time - boost_time < 10:
                current_globals.fps = 5
            else:
                current_globals.fps = 60
                time_boosted = False

            PygameGlobals.fpsClock.tick(current_globals.fps)

            if collision_speed_boost:
                speed_boost_time = time.time()
                player_speed = PygameGlobals.all_settings['player_speed'] * 2

            elif speed_boost_time is None or current_time - speed_boost_time > 10:
                player_speed = PygameGlobals.all_settings['player_speed']

            if self.state == 'game_over':
                self.game_over()

    def game_over(self):
        PygameGlobals.screen.fill((0, 0, 0))
        PygameGlobals.screen.blit(PygameGlobals.game_over_image, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.state = 'menu'

            pygame.display.flip()
            PygameGlobals.fpsClock.tick(PygameGlobals.fps)

            if self.state == 'menu':
                self.menu()

    def menu(self):
        # Widgets(left, top, text)
        play_button = Widget(PygameGlobals.width // 10, PygameGlobals.height // 3, 'play')
        quit_button = Widget(PygameGlobals.width // 10, PygameGlobals.height // 2.4, 'quit')
        music_off_button = Widget(PygameGlobals.width // 10, PygameGlobals.height // 2, 'toggle music')
        garage_button = Widget(PygameGlobals.width // 10, PygameGlobals.height // 1.7, 'garage')

        PygameGlobals.screen.fill((0, 0, 0))
        PygameGlobals.screen.blit(play_button.font_surface, (play_button.x, play_button.y))
        PygameGlobals.screen.blit(quit_button.font_surface, (quit_button.x, quit_button.y))
        PygameGlobals.screen.blit(music_off_button.font_surface,
                                  (music_off_button.x, music_off_button.y))
        PygameGlobals.screen.blit(garage_button.font_surface,
                                  (garage_button.x, garage_button.y))

        while True:
            mouse_x, mouse_y = None, None
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                if event.type == pygame.QUIT:
                    quit_game()

            if mouse_x is not None:
                if play_button.collidepoint(mouse_x, mouse_y):
                    self.state = 'main_game'
                if quit_button.collidepoint(mouse_x, mouse_y):
                    quit_game()
                if music_off_button.collidepoint(mouse_x, mouse_y):
                    if not current_globals.music_stopped:
                        pygame.mixer.music.stop()
                        current_globals.music_stopped = True
                    else:
                        current_globals.music_stopped = False
                        pygame.mixer.music.play(-1)
                if garage_button.collidepoint(mouse_x, mouse_y):
                    self.state = 'garage'

            pygame.display.flip()
            PygameGlobals.fpsClock.tick(PygameGlobals.fps)

            if self.state == 'main_game':
                self.main_game()

            elif self.state == 'garage':
                self.garage()

    def garage(self):
        # Widgets(left, top, text)
        buttons = [
            Widget(PygameGlobals.width // 15, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width // 6, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width * 0.25, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width * 0.33, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width * 0.40, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width * 0.48, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width * 0.56, PygameGlobals.height // 3, 'buy'),
            Widget(PygameGlobals.width // 15, PygameGlobals.height * 0.66, 'menu')
        ]
        use_buttons = [
            Widget(PygameGlobals.width // 15, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width // 6, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width * 0.25, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width * 0.33, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width * 0.40, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width * 0.48, PygameGlobals.height // 5, 'use'),
            Widget(PygameGlobals.width * 0.56, PygameGlobals.height // 5, 'use')
        ]
        car2 = get_car_image('car2.png')
        car3 = get_car_image('car3.png')
        car4 = get_car_image('car4.png')
        car5 = get_car_image('car5.png')
        car6 = get_car_image('car6.png')
        car6 = pygame.transform.scale(car6, (PygameGlobals.width // 20, PygameGlobals.height // 8))

        car7 = get_car_image('car7.png')
        car8 = get_car_image('car8.png')

        car_images = [
            car2, car3, car4,
            car5, car6, car7, car8
        ]

        PygameGlobals.screen.fill((0, 0, 0))

        money_amount_font = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
            18)
        money_amount_surf = money_amount_font.render(
            str(PygameGlobals.all_settings['player_money']), True, (255, 255, 255))

        money_icon = pygame.image.load(os.path.join(PygameGlobals.MEDIA_DIR, 'dollar.png'))
        money_icon = pygame.transform.scale(
            money_icon, (PygameGlobals.width // 50, PygameGlobals.height // 40))
        PygameGlobals.screen.blit(money_icon, (PygameGlobals.width * 0.75, PygameGlobals.height * 0.75))
        PygameGlobals.screen.blit(money_amount_surf, (PygameGlobals.width * 0.72, PygameGlobals.height * 0.75))

        for button in buttons:
            PygameGlobals.screen.blit(button.font_surface, (button.x, button.y))

        for use_button in use_buttons:
            PygameGlobals.screen.blit(use_button.font_surface, (use_button.x, use_button.y))

        for i in range(len(car_images)):
            car_image = car_images[i]
            PygameGlobals.screen.blit(car_image, (buttons[i].x, buttons[i].y + PygameGlobals.height // 7))

        while True:
            mouse_x, mouse_y = None, None
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                if event.type == pygame.QUIT:
                    quit_game()

            if mouse_x is not None:
                for i in range(len(buttons)):
                    button = buttons[i]
                    if button.collidepoint(mouse_x, mouse_y):
                        if i == len(buttons) - 1:
                            self.state = 'menu'
                        else:
                            surf = pygame.Surface((PygameGlobals.width // 2, PygameGlobals.height // 7))
                            surf.fill((0, 0, 0))
                            PygameGlobals.screen.blit(surf, (0, 0))
                            buy_car(i + 2)
                            money_amount_font.render(
                                str(PygameGlobals.all_settings['player_money']), True, (255, 255, 255)
                            )

                for i in range(len(use_buttons)):
                    button = use_buttons[i]
                    if button.collidepoint(mouse_x, mouse_y):
                        surf = pygame.Surface((PygameGlobals.width // 2, PygameGlobals.height // 7))
                        surf.fill((0, 0, 0))
                        PygameGlobals.screen.blit(surf, (0, 0))
                        use_car(i + 2)

            pygame.display.flip()
            PygameGlobals.fpsClock.tick(PygameGlobals.fps)

            if self.state == 'menu':
                self.menu()


def main():
    current_state = GameState()
    current_state.menu()


if __name__ == '__main__':
    main()
