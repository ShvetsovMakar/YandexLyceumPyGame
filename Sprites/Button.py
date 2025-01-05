import pygame

from Sprites.Label import Label


class Button(Label):
    def __init__(self, image_path, hovered_over_image_path, position, size, sprite_group, on_click):
        super().__init__(image_path, position, size, sprite_group)

        self.on_click = on_click

        self.basic_image_path = image_path
        self.hovered_over_image_path = hovered_over_image_path

    def set_hovered_on_image(self):
        self.change_image(self.hovered_over_image_path)

    def set_basic_image(self):
        self.change_image(self.basic_image_path)
