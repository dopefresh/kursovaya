# import json
# settings = open("settings.txt", "r", encoding="utf-8")
# all_settings = json.loads(settings.read())
# settings.close()
# print(all_settings)
import random


class SomeClass:
    def __init__(self, **kwargs):
        self.a = kwargs['a']


class AnotherClass:
    def __init__(self, **kwargs):
        self.b = kwargs['b']



kwargs = {'a': 5, 'b': 3}
random_class = random.choice([SomeClass, AnotherClass])
random_example = random_class(**kwargs)
print(random_example.__dict__)







