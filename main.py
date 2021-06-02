import pygame
from pygame.locals import *

import sys
import time
import random


# Globals and initialization
SCORES = []
pygame.init()
begin_time = time.time()
fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 650
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drag Racing")

# Game images
background_image = pygame.image.load('road.png')
background_image = pygame.transform.scale(background_image, (width, height))
game_over_image = pygame.image.load('game_over.png')
game_over_image = pygame.transform.scale(game_over_image, (width, height))

# Music
pygame.mixer.init()
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)
music_stopped = False


def quit_game():
    global SCORES
    output = open("data.txt", "w", encoding="utf-8")
    for score in SCORES:
        output.write(f"{score}\n")
    exit()


class Widget(pygame.Rect):
    def __init__(self, left, top, width, height, text, screen):
        super().__init__((left, top), (width, height))
        self.font = pygame.font.Font('FiraCodeBold.ttf', 18)
        self.screen = screen
        self.font_surface = self.font.render(text, True,
                                             (255, 255, 255))


class Car(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed_y = 0

    def update(self):
        self.rect.y += self.speed_y


class Player(Car):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.rect.x = width // 2
        self.rect.y = height - self.rect.height
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x < width // 6:
            self.rect.x = width // 6
        if self.rect.x > width - width // 6 - self.rect.width:
            self.rect.x = width - self.rect.width - width // 6
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > height - self.rect.height:
            self.rect.y = height - self.rect.height

    def ride(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0


class Enemy(Car):
    def __init__(self, image_path, x, y):
        super().__init__(image_path)
        self.rect.x = x
        self.rect.y = y

    def update(self, speed_y):
        self.speed_y = speed_y
        self.rect.y += self.speed_y
        if self.rect.y > height:
            self.kill()


class GameState:
    def __init__(self):
        self.state = 'menu'

    def main_game(self):
        global screen, width, height
        prev_time = time.time()

        # Sprites
        player = Player('ltblue_car.png')
        players = pygame.sprite.Group()
        players.add(player)
        enemies = pygame.sprite.Group()
        enemy_speed = 20

        # Score

        score_number = 0
        score = pygame.font.Font('FiraCodeBold.ttf', 25)
        score_surf = score.render(str(score_number), True, (255, 255, 255))

        while True:
            screen.fill((0, 0, 0))
            screen.blit(background_image, (0, 0))
            screen.blit(score_surf, (0, 0))

            current_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    SCORES.append(score_number)
                    quit_game()

                if event.type == KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.ride(-20, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.ride(20, 0)
                    elif event.key == pygame.K_UP:
                        player.ride(0, -20)
                    elif event.key == pygame.K_DOWN:
                        player.ride(0, 20)
                if event.type == KEYUP:
                    player.stop()

            if current_time - prev_time >= 0.5:
                prev_time = current_time
                enemy = Enemy('blue_car.png', random.randint(
                    width // 6, width - width // 6), -100)
                enemies.add(enemy)
                score_number += 1
                score_surf = score.render(
                    str(score_number), True, (255, 255, 255))

            players.draw(screen)
            players.update()

            enemies.draw(screen)
            if (current_time - begin_time) % 10 == 0:
                enemy_speed += 1
                if enemy_cars < 7:
                    enemy_cars += 1

            enemies.update(enemy_speed)
            collision = pygame.sprite.groupcollide(
                enemies, players, False, True)
            if collision:
                SCORES.append(score_number)
                self.state = 'game_over'

            pygame.display.flip()
            fpsClock.tick(fps)

            if self.state == 'game_over':
                self.game_over()
            elif self.state == 'menu':
                self.menu()

    def game_over(self):
        global screen, game_over_background
        screen.fill((0, 0, 0))
        screen.blit(game_over_image, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.state = 'menu'

            pygame.display.flip()
            fpsClock.tick(fps)

            if self.state == 'main_game':
                self.main_game()
            elif self.state == 'menu':
                self.menu()

    def menu(self):

        global screen, music_stopped
        # Widgets
        play_button = Widget(width // 10, height // 3, width //
                             15, height // 15, 'play', screen)
        quit_button = Widget(width // 10, height // 2.4, width //
                             15, height // 15, 'quit', screen)
        music_off_button = Widget(width // 10, height // 2,
                                  width // 15, height // 15, 'toggle music', screen)
        screen.fill((0, 0, 0))
        screen.blit(play_button.font_surface, (play_button.x, play_button.y))
        screen.blit(quit_button.font_surface, (quit_button.x, quit_button.y))
        screen.blit(music_off_button.font_surface,
                    (music_off_button.x, music_off_button.y))

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
                    if not music_stopped:
                        pygame.mixer.music.stop()
                        music_stopped = True
                    else:
                        music_stopped = False
                        pygame.mixer.music.play(-1)

            pygame.display.flip()
            fpsClock.tick(fps)

            if self.state == 'main_game':
                self.main_game()
            elif self.state == 'game_over':
                self.game_over()


if __name__ == '__main__':
    current_state = GameState()
    current_state.menu()
