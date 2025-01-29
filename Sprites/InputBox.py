import pygame

from Sprites.TextBox import TextBox


class InputBox(TextBox):
    def __init__(self, text, font, size, position, max_length, sprite_group,
                 text_color, background_color=None, active_color=None, outline_color=None):
        super().__init__(text, font, position, sprite_group,
                         text_color, background_color, outline_color)

        self.max_length = max_length
        self.active = False

        self.width = size[0]
        self.height = size[1]

        self.active_color = active_color

    def draw(self, screen):
        if self.background_color is not None:
            if self.active:
                pygame.draw.rect(screen, self.active_color,
                                 (self.x - 5, self.y - 5,
                                  self.width + 10, self.height + 10),
                                 0)

            else:
                pygame.draw.rect(screen, self.background_color,
                                 (self.x - 5, self.y - 5,
                                  self.width + 10, self.height + 10),
                                 0)

        if self.outline_color is not None:
            pygame.draw.rect(screen, self.outline_color,
                             (self.x - 5, self.y - 5,
                              self.width + 10, self.height + 10),
                             2)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x, self.y))
