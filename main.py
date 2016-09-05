'''
Main file of the game: Implementation of the Interface with pygame
'''

import pygame
from game import Game2048
from pygame_window import PyGameWindow

if __name__ == '__main__':
    pygame.init()
    game2048 = Game2048()
    pygameWindow = PyGameWindow(game2048)
    pygameWindow.launch()
    pygame.quit()

    
    