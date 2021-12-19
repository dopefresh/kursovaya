import os

import pygame

from project.main import FONT_DIR, width, height, screen


class Widget(pygame.Rect):
    def __init__(self, left, top, text):
        super().__init__((left, top), (width // 15, height // 15))
        self.font = pygame.font.Font(
            os.path.join(FONT_DIR, 'FiraCodeBold.ttf'),
            18
        )
        self.screen = screen
        self.font_surface = self.font.render(
            text,
            True,
            (255, 255, 255)
        )