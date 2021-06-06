import json
settings = open("settings.txt", "r", encoding="utf-8")
all_settings = json.loads(settings.read())
settings.close()
print(all_settings)


