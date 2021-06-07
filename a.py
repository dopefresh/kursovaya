import json
settings = open("settings.txt", "r", encoding="utf-8")
all_settings = json.loads(settings.read())
settings.close()

settings_write = open("settings.txt", "w", encoding="utf-8")
print(json.dumps(all_settings))
settings_write.write(json.dumps(all_settings))







