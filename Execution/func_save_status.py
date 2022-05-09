import json


def save_status(dict):
    with open("status.json", "w") as fp:
        json.dump(dict, fp, indent=4)
# indent makes the file more readable, without it, it writes everything on a single line.
