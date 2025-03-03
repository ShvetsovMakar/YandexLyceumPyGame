import pygame

from Config.Characteristics.Breastplates import *


class Breastplate(pygame.sprite.Sprite):
    def __init__(self, name, level, sprite_group, size, position):
        super().__init__(sprite_group)

        self.type = name

        # Setting up breastplate image
        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(f"Graphics/Characters/Breastplates/{self.type}.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        # Setting up breastplate characteristics
        data = BREASTPLATES[self.type]

        self.level = level
        self.protection = data["protection"] * BREASTPLATE_ENHANCEMENT ** self.level
        self.agility = data["agility"]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
