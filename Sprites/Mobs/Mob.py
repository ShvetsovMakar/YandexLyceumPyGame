import pygame


# This class is very similar to Label class, yet it is going to get different in process of game development
class Mob(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size, sprite_group):
        super().__init__(sprite_group)

        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
