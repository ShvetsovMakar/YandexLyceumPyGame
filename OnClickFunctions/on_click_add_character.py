import os
import json

from Config.constants import *


def forward(index, name):
    return False, (index + 1) % 4


def backward(index, name):
    return False, (index - 1) % 4


def to_main_menu(index, name):
    return (True, )


def create_character(index, name):
    if not name:
        return False, index

    filenames = os.listdir("Data/Characters")
    character_names = []

    for filename in filenames:
        if os.path.splitext(filename)[-1] == ".json":
            character_names.append(os.path.splitext(filename)[0])

    if name in character_names:
        return False, index

    character_data = {"name": name,
                      "skin": CHARACTER_NAMES[index],
                      "level": 1,
                      "XP": 0,
                      "gear": {
                          "weapon": {
                              "type": None,
                              "level": None
                          },
                          "armor": {
                              "helmet": {
                                  "type": None,
                                  "level": None
                              },
                              "breastplate": {
                                  "type": None,
                                  "level": None
                              },
                              "leggings": {
                                  "type": None,
                                  "level": None
                              }
                          }
                      },
                      "gold": 0,
                      "inventory": []
                      }

    with open(f"Data/Characters/{name}.json", "w") as file:
        json.dump(character_data, file, indent=4)

    return (True, )
