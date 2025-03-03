import pygame


# This class is very similar to Label class, yet it is going to get different in process of game development
class Mob(pygame.sprite.Sprite):
    def __init__(self, frames, position, size, sprite_group):
        super().__init__(sprite_group)

        self.width = size[0]
        self.height = size[1]
        
        self.frames = frames
        image = pygame.image.load(frames[0])
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.animation_counter = 0
        self.frame_index = 0

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def change_image(self, image_path):
        x = self.rect.x
        y = self.rect.y

        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.animation_counter += 1
        self.animation_counter %= 11

        if self.animation_counter == 0:
            self.frame_index += 1
            self.frame_index %= len(self.frames)
            
            self.change_image(self.frames[self.frame_index])
