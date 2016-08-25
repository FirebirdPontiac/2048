'''
Implementation of the Game2048 class that will handle the 2048 game
'''

import numpy as np
from random import randint

class Game2048(object):
    
    def __init__(self, grid_dim=4):
        '''
        Initializes the grid of the game and the list of possible moves
        grid_dim -- int
            the dimension of the grid
        '''
        self.dim = grid_dim
        self.score = 0
        # Initialization of the grid with two random squares
        self.grid = np.zeros((self.dim, self.dim), dtype=int)
        tup = self.add_square()
        tup = self.add_square()
        # Initialization of a list of possible moves:
        self.possible_moves = []
        self.find_possible_moves()

    def update_score(self):
        self.score = np.amax(self.grid)

    def game_won(self):
        return (self.score == 2048)

    def game_over(self):
        return (len(self.possible_moves) == 0)

    def add_square(self):
        '''
        Adds a square at random in the grid. The added square takes values:
            2 with probability 0.8
            4 with probability 0.2
        Returns
        -------
        (i,j) -- tuple
            The indices of the square to insert in the grid
        '''
        zeros_indices = np.where(self.grid == 0)
        nb_indices = zeros_indices[0].shape[0]
        index = randint(0, nb_indices-1)
        proba = np.random.uniform(0.0,1.0)
        value = 2
        if proba > 0.8:
            value = 4
        self.grid[zeros_indices[0][index]][zeros_indices[1][index]] = value
        return (zeros_indices[0][index],zeros_indices[1][index])

    def find_possible_moves(self):
        '''
        Find the possible moves in the grid
        '''
        dico = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        for i in range(self.dim):
            for j in range(self.dim):
                # (i,j) is the cell we look at
                neighbors = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
                for k in range(4):
                    # tup is the neighbor of (i,j) we look at
                    tup = neighbors[k]
                    if (tup[0] in range(self.dim) and tup[1] in range(self.dim)):
                        if self.grid[i][j] > 0:
                            if self.grid[tup[0]][tup[1]] in [0, self.grid[i][j]]:
                                if k == 0:
                                    dico['UP'] = True
                                elif k == 1:
                                    dico['DOWN'] = True
                                elif k == 2:
                                    dico['LEFT'] = True
                                elif k == 3:
                                    dico['RIGHT'] = True
        # update the possible_moves list:
        self.possible_moves = []
        for key in dico.keys():
            if dico[key]:
                self.possible_moves.append(key)

    def move_grid(self, move):
        '''
        Upgrades the grid with the move move. Here we suppose that the move
        is in self.possible_moves.
        move -- string
            possible move for the grid
        Returns
        -------
        moves -- list
            list of all the moves that have been made during that function
            elements of the list : ((i,j), (i',j')) where:
                (i,j) is the source of the square
                (i',j') is the destination of the square
        '''
        if move in self.possible_moves:
            # Initializes the list of moves as an empty list:
            moves = []

            # Define the direction of move, depending on move:
            # Also define the order to which we go through the grid:
            if move == 'UP':
                dir_i = -1
                dir_j = 0
                range_i = range(self.dim)
                range_j = range(self.dim)
            elif move == 'DOWN':
                dir_i = 1
                dir_j = 0
                range_i = range(self.dim-1,-1,-1)
                range_j = range(self.dim)
            elif move == 'LEFT':
                dir_i = 0
                dir_j = -1
                range_i = range(self.dim)
                range_j = range(self.dim)
            elif move == 'RIGHT':
                dir_i = 0
                dir_j = 1
                range_i = range(self.dim)
                range_j = range(self.dim-1,-1,-1)

            # First we move all the squares we can and save the moves.
            # For e.g., if move == 'RIGHT', we begin to move the squares of the
            # right of the grid, and till the squares form the left.
            
            for i in range_i:
                for j in range_j:
                    if self.grid[i][j] != 0:
                        n_i = i
                        n_j = j
                        while True:
                            tup = (n_i+dir_i, n_j+dir_j)
                            if (tup[0] not in range(self.dim)) \
                                    or (tup[1] not in range(self.dim)):
                                value = self.grid[i][j]
                                self.grid[i][j] = 0
                                self.grid[n_i][n_j] = value
                                if (i!=n_i) or (j!=n_j):
                                    moves.append(((i,j),(n_i,n_j)))
                                break
                            elif self.grid[tup[0]][tup[1]] == 0:
                                n_i = tup[0]
                                n_j = tup[1]
                            elif (self.grid[i][j] == self.grid[tup[0]][tup[1]]):
                                if (tup[0],tup[1]) not in [el[1] for el in moves]:
                                    self.grid[tup[0]][tup[1]]*=2
                                    self.grid[i][j] = 0
                                    moves.append(((i,j),(tup[0],tup[1])))
                                else:
                                    if (n_i != i) or (n_j != j):
                                        self.grid[n_i][n_j] = self.grid[i][j]
                                        self.grid[i][j] = 0
                                        moves.append(((i,j),(n_i,n_j)))
                                break
                            elif (self.grid[i][j] != self.grid[tup[0]][tup[1]]) and \
                                    (self.grid[tup[0]][tup[1]] != 0):
                                if (n_i != i) or (n_j != j):
                                    self.grid[n_i][n_j] = self.grid[i][j]
                                    self.grid[i][j] = 0
                                    moves.append(((i,j),(n_i,n_j)))
                                break

            return moves







