from abc import ABC, abstractmethod

from project.pygame_globals import width, height


class MoveBehavior(ABC):
    @abstractmethod
    def move(self, obj):
        pass


class MoveYBehavior(MoveBehavior):
    def move(self, obj):
        obj.rect.y += obj.speed_y
        if obj.rect.y < obj.rect.height // 5:
            obj.rect.y = obj.rect.height // 5
        if obj.rect.y > height - obj.rect.height:
            obj.rect.y = height - obj.rect.height


class MoveXBehavior(MoveBehavior):
    def move(self, obj):
        obj.rect.x += obj.speed_x

        if obj.rect.x < width // 10:
            obj.rect.x = width // 10
        if obj.rect.x > width - width // 3 - obj.rect.width - width // 9:
            obj.rect.x = width - obj.rect.width - width // 3 - width // 9


class MoveYEnemyBehavior(MoveBehavior):
    def move(self, obj, speed_y):
        obj.speed_y = speed_y
        obj.rect.y += obj.speed_y
        if obj.rect.y > height:
            obj.kill()
