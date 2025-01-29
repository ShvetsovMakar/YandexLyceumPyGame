import pygame
import sys
import os


def exit(game):
    pygame.quit()
    sys.exit()

def add_character(game):
    game.add_character()


def play(game):
    if not os.listdir("Data/Characters"):
        game.add_character()
    else:
        game.choose_character()
