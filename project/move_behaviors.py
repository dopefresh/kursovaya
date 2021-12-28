from abc import ABC, abstractmethod

from project.pygame_globals import PygameGlobals

from typing import final


class MoveBehavior(ABC):
    @abstractmethod
    def move(self, obj):
        pass


@final
class MoveYBehavior(MoveBehavior):
    def move(self, obj):
        obj.rect.y += obj.speed_y
        if obj.rect.y < obj.rect.height // 5:
            obj.rect.y = obj.rect.height // 5
        if obj.rect.y > PygameGlobals.height - obj.rect.height:
            obj.rect.y = PygameGlobals.height - obj.rect.height


@final
class MoveXBehavior(MoveBehavior):
    def move(self, obj):
        obj.rect.x += obj.speed_x
        if obj.rect.x < PygameGlobals.width // 10:
            obj.rect.x = PygameGlobals.width // 10
        if obj.rect.x > PygameGlobals.width - PygameGlobals.width // 3 - obj.rect.width - PygameGlobals.width // 9:
            obj.rect.x = PygameGlobals.width - obj.rect.width - PygameGlobals.width // 3 - PygameGlobals.width // 9


@final
class MoveYEnemyBehavior(MoveBehavior):
    def move(self, obj, speed_y):
        obj.speed_y = speed_y
        obj.rect.y += obj.speed_y
        if obj.rect.y > PygameGlobals.height:
            obj.kill()
