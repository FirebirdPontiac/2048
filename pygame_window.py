'''
Implementation of the PyGameWindow object that handles the game 2048 with 
Pygame. Uses the class Game2048 to handle the game
'''

import pygame
import numpy as np
import sys
import time
from game import Game2048

# Dictionary to point to .png path for each value:
square_numbers = {}
for i in range(11):
    value = 2 ** (i+1)
    square_numbers[value] = 'images/'+str(value)+'.png'

class PyGameWindow(object):
    
    def __init__(self, game2048):
        '''
        game2048 -- Game2048 object
        '''
        # Parameters of the 2048 game:
        self.game2048 = game2048
        self.grid_dim = self.game2048.dim
        self.grid = self.game2048.grid # actual grid
        self.new_grid = np.zeros(shape=(self.grid_dim, self.grid_dim)) # new grid
        # Parameters for Pygame window display :
        self.size = 450,450  # Size of the Pygame window
        self.black = 0, 0, 0 
        self.white = 255,255,255
        self.red = 255,0,0
        self.green = 0,255,0
        self.WIDTH = 100 # width of a square
        self.HEIGHT = 100 # height of a square
        self.MARGIN = 10 # margin of a square
        self.speed = 2 # speed of a digit when moving
        # Parameters of the numbers images:
        self.numbers = {}  # pygame.image objects for every square in the game
        self.numberrects = {} # number.get_rect() for every square in the game
        self.moves = [] # the moves for every numbers that are moving
    
    def launch(self):
        '''
        Initialization of the Window and lanches the menu screen
        '''
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('2048 Game')
        # Fill background:
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.black)
        # Display text:
        font = pygame.font.Font(None, 36)
        text = font.render("Let's play 2048", 1, self.white)
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = int(0.2*self.background.get_rect().centery)
        self.background.blit(text, textpos)
        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        counter = 5
        actual_time = time.time()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if (time.time()-actual_time) > 1.0:
                actual_time = time.time()
                counter -= 1
                if counter > 0 :
                    # Refresh the background (to delete previous counters)
                    self.background.fill(self.black)
                    # 2048 text:
                    font = pygame.font.Font(None, 36)
                    text = font.render("Let's play 2048", 1, self.white)
                    textpos = text.get_rect()
                    textpos.centerx = self.background.get_rect().centerx
                    textpos.centery = int(0.2*self.background.get_rect().centery)
                    self.background.blit(text, textpos)
                    # Counter text:
                    counter_font = pygame.font.Font(None, 144)
                    text_counter = counter_font.render(str(counter), 1, self.red)
                    text_counter_pos = text.get_rect()
                    text_counter_pos.centerx = 0.6*self.size[0]
                    text_counter_pos.centery = 0.4*self.size[1]
                    self.background.blit(text_counter, text_counter_pos)
                    self.screen.blit(self.background, (0, 0))
                    pygame.display.flip()
                else:
                    self.play()
                    break
            
    def play(self):
        '''
        Play the game !
        '''
        while 1:
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.moves = self.game2048.move_grid('UP')
                        self.new_grid = self.game2048.grid
                    elif event.key == pygame.K_DOWN:
                        self.moves = self.game2048.move_grid('DOWN')
                        self.new_grid = self.game2048.grid
                    elif event.key == pygame.K_RIGHT:
                        self.moves = self.game2048.move_grid('RIGHT')
                        self.new_grid = self.game2048.grid
                    elif event.key == pygame.K_LEFT:
                        self.moves = self.game2048.move_grid('LEFT')
                        self.new_grid = self.game2048.grid
            # Refresh the screen:
            self.screen.fill(self.black)
            # Plot the empty grid : 
            for row in range(4):
                for column in range(4):
                    color = self.white
                    pygame.draw.rect(self.screen,
                                     color,
                                     [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                      (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                      self.WIDTH,
                                      self.HEIGHT])
            # If no actual moves, blit the numbers to the screen:
            if self.moves == []:
                self.numbers = {}
                self.numberrects = {}
                for i in range(self.grid_dim):
                    for j in range(self.grid_dim):
                        value = self.grid[i][j]
                        if value != 0:
                            number = pygame.image.load(square_numbers[value])
                            number = pygame.transform.scale(number, (self.WIDTH, self.HEIGHT))
                            self.numbers[(i,j)] = number
                            numberrect = number.get_rect()
                            numberrect.centerx = self.MARGIN*(j+1)+self.WIDTH*j+self.WIDTH/2
                            numberrect.centery = self.MARGIN*(i+1)+self.HEIGHT*i+self.HEIGHT/2
                            self.numberrects[(i,j)] = numberrect
                            self.screen.blit(number, numberrect)
                # If game over or game won, break the loop and print win or lose
                if self.game2048.game_won() or self.game2048.game_over():
                    pygame.display.flip()
                    break
            else:
                to_delete = []
                for k in range(len(self.moves)):
                    tup = self.moves[k]
                    tup1 = tup[0]
                    tup2 = tup[1]
                    number = self.numbers[tup1]
                    # find the speed:
                    speed = np.array([0,0])
                    valx = tup2[0]-tup1[0]
                    if valx != 0:
                        speed[0] = int(np.sign(valx))
                    valy = tup2[1]-tup1[1]
                    if valy != 0:
                        speed[1] = int(np.sign(valy))
                    speed = list(speed)
                    speed_i, speed_j = speed
                    speed = [speed_j, speed_i]
                    # Check if the square is at position tup2:
                    numberrect = self.numberrects[tup1]
                    i = tup2[0]
                    j = tup2[1]
                    boolean = (numberrect.centerx == \
                                self.MARGIN*(j+1)+self.WIDTH*j+self.WIDTH/2) \
                              and \
                              (numberrect.centery == \
                                self.MARGIN*(i+1)+self.HEIGHT*i+self.HEIGHT/2)
                    if boolean:
                        to_delete.append(k)
                    else:
                        numberrect = numberrect.move(speed)
                        self.numberrects[tup1] = numberrect
                if to_delete != []:
                    new_list = []
                    for i in range(len(self.moves)):
                        if i not in to_delete:
                            new_list.append(self.moves[i])
                    self.moves = new_list
                # Blit the squares to the screen:
                for tup in self.numbers.keys():
                    number = self.numbers[tup]
                    numberrect = self.numberrects[tup]
                    self.screen.blit(number, numberrect)
                if self.moves == []:
                    self.game2048.add_square()
                    self.game2048.find_possible_moves()
            pygame.display.flip()
        
        if self.game2048.game_over():
            time.sleep(1.0)
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER", 1, self.red)
            textpos = text.get_rect()
            textpos.centerx = self.size[0]/2
            textpos.centery = self.size[0]*3/8
            self.screen.blit(text, textpos)
            pygame.display.flip()
            time.sleep(2.0)
        elif self.game2048.game_won():
            time.sleep(1.0)
            font = pygame.font.Font(None, 72)
            text = font.render("YOU WIN!", 1, self.green)
            textpos = text.get_rect()
            textpos.centerx = self.size[0]/2
            textpos.centery = self.size[0]*3/8
            self.screen.blit(text, textpos)
            pygame.display.flip()
            time.sleep(2.0)
            
        while 1:
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    sys.exit()
            








