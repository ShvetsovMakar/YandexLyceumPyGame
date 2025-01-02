import pygame


class Label(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size, sprite_group):
        super().__init__(sprite_group)

        self.image_path = image_path

        self.width = size[0]
        self.height = size[1]

        image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
