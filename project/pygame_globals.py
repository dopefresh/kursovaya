import pygame

import time
import json
import os
from pathlib import Path
from typing import List


class PygameGlobals:
    """
    Singleton for accessing and modifying pygame globals
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    CARS: List[str] = ['car1.png', 'car2.png', 'car3.png', 'car4.png',
                       'car5.png', 'car6.png', 'car7.png', 'car8.png']

    BASE_DIR = Path(__file__).resolve().parent
    MEDIA_DIR = os.path.join(BASE_DIR, "media")
    MUSIC_DIR = os.path.join(BASE_DIR, "music")
    FONT_DIR = os.path.join(BASE_DIR, "fonts")
    with open(os.path.join(BASE_DIR, "settings.txt")) as settings:
        all_settings: dict = json.loads(settings.read())

    SCORES: List[int] = []
    pygame.init()
    begin_time: float = time.time()
    fps: int = all_settings['fps']
    fpsClock: pygame.time.Clock = pygame.time.Clock()

    width, height = all_settings["width"], all_settings["height"]
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Drag Racing")
    pygame.display.set_icon(pygame.image.load(
        os.path.join(MEDIA_DIR, "icon.png"))
    )
    # Game images
    game_over_image = pygame.image.load(
        os.path.join(MEDIA_DIR, "game_over.png")
    )
    game_over_image = pygame.transform.scale(
        game_over_image,
        (width, height)
    )

    # Music
    pygame.mixer.init()
    pygame.mixer.music.load(
        os.path.join(MUSIC_DIR, "music.wav")
    )
    pygame.mixer.music.play(-1)
    music_stopped = False

    background_image = pygame.image.load(
        os.path.join(MEDIA_DIR, 'road2.png')
    )
    background_image = pygame.transform.scale(
        background_image,
        (width - width // 3, height * 2)
    )
    mountains = pygame.image.load(
        os.path.join(MEDIA_DIR, 'mountains.png')
    )
    mountains = pygame.transform.rotate(mountains, 270)
    mountains = pygame.transform.scale(mountains, (width // 3, height * 2))

    def set_music_stopped(self, flag: bool):
        self.music_stopped = flag


