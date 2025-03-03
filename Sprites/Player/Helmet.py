import pygame

from Config.Characteristics.Helmets import *


class Helmet(pygame.sprite.Sprite):
    def __init__(self, name, level, sprite_group, size, position):
        super().__init__(sprite_group)

        self.type = name

        # Setting up helmet image
        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(f"Graphics/Characters/Helmets/{self.type}.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Setting up helmet characteristics
        data = HELMETS[self.type]

        self.level = level
        self.protection = data["protection"] * HELMET_ENHANCEMENT ** self.level
        self.agility = data["agility"]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
