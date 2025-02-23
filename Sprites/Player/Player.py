import pygame
import json


class Player(pygame.sprite.Sprite):
    def __init__(self, name, sprite_group, size, position):
        super().__init__(sprite_group)

        self.name = name

        self.width = size[0]
        self.height = size[1]

        self.x = position[0]
        self.y = position[1]

        with open(f"Data/Characters/{self.name}.json", "r") as file:
            data = json.load(file)



