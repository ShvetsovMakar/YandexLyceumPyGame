import pygame
import json


class Player(pygame.sprite.Sprite):
    def __init__(self, name, sprite_group, size, position):
        super().__init__(sprite_group)

        self.name = name

        self.width = size[0]
        self.height = size[1]

        with open(f"Data/Characters/{self.name}.json", "r") as file:
            data = json.load(file)

            self.head_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Heads/{data['skin']}.png"),
                                                     (self.width, self.height))

            self.rect = self.head_image.get_rect()
            self.rect.x = position[0]
            self.rect.y = position[1]

            self.torso_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Torsos/{data['skin']}.png"),
                                                     (self.width, self.height))

            self.legs_image = pygame.transform.scale(pygame.image.load(f"Graphics/Characters/Legs/{data['skin']}.png"),
                                                     (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.torso_image, self.rect)
        screen.blit(self.legs_image, self.rect)
        screen.blit(self.head_image, self.rect)



