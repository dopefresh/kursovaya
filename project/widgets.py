import pygame

from project.pygame_globals import PygameGlobals

from typing import final
import os


@final
class Widget(pygame.Rect):
    def __init__(self, left, top, text):
        super().__init__((left, top), (PygameGlobals.width // 15, PygameGlobals.height // 15))
        self.font = pygame.font.Font(
            os.path.join(PygameGlobals.FONT_DIR, 'FiraCodeBold.ttf'),
            18
        )
        self.screen = PygameGlobals.screen
        self.font_surface = self.font.render(
            text,
            True,
            (255, 255, 255)
        )
