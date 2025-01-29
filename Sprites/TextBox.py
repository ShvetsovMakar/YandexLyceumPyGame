import pygame


class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, font, position, sprite_group,
                 text_color, background_color=None, outline_color=None):
        super().__init__(sprite_group)

        self.text = text

        self.font = font

        self.x = position[0]
        self.y = position[1]

        self.text_color = text_color
        self.background_color = background_color
        self.outline_color = outline_color

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.text_color)
        width = text_surface.get_width()
        height = text_surface.get_height()

        if self.background_color is not None:
            pygame.draw.rect(screen, self.background_color,
                             (self.x - width // 2 - 5, self.y - 5,
                              width + 10, height + 10),
                             0)

        if self.outline_color is not None:
            pygame.draw.rect(screen, self.outline_color,
                             (self.x - width // 2 - 5, self.y - 5,
                              width + 10, height + 10),
                             2)

        screen.blit(text_surface, (self.x - width // 2, self.y))

    def change_text(self, new_text):
        self.text = new_text
