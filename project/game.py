"""
This module contains the game logic for Tic Tac Toe and Gomoku. 
* You may need to understand the code to implement your own players. 
! The code should not be modified.
"""
from typing import List, Optional
from abc import ABC, abstractmethod
from .player import Player

class Game(ABC):
    
    @abstractmethod
    def empty_cells(self, state: Optional[List[List[int]]]) -> List[List[int]]:
        """
        Get a list of empty cells for the GIVEN state. If state is None, return the list of empty cells for the CURRENT state.
        :param state: the state of the current board
        :return: a list of empty cells
        """
        pass
    
    @abstractmethod
    def print_board(self):
        """
        Visualization of current board state.
        """
        pass
    
    @abstractmethod
    def init_board(self):
        """
        Draw the initial board and show the game info.
        """
        pass
    
    @abstractmethod
    def valid_move(self, x: int, y: int) -> bool:
        """
        Check if the cell (x,y) is a valid move.
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the move is valid
        """
        pass
    
    @abstractmethod
    def set_move(self, x: int, y: int, player: Player) -> bool:
        """
        Set the move on board, if the coordinates are valid.
        :param x: X coordinate
        :param y: Y coordinate
        :param player: player
        :return: True if the move is set successfully
        """
        pass

    @abstractmethod
    def wins(self, player: Player, state: Optional[List[List[int]]]) -> bool:
        """
        This function tests if a specific player wins in a GIVEN or CURRENT state (if state is None).
        :param state: the state of the current board
        :param player: player
        :return: True if the player wins
        """
        pass
        
    @abstractmethod
    def game_over(self) -> bool:
        """
        This function test if the game is over for the current state
        :return: True if the game is over (either a player wins or the game is draw)
        """
        pass
    
class TicTacToe(Game):
    def __init__(self):
        #* Initialize board, available moves, and last move
        self.board_state = [[None, None, None], [None, None, None], [None, None, None]]
        self.avail_moves = {(i, j) for j in range(3) for i in range(3)}
        self.last_move = None
    
    def print_board(self):
        height = len(self.board_state)
        width = len(self.board_state[0])
        
        for i in range(height):
            print('-------------')
            for j in range(width):
                if self.board_state[i][j] == None:
                    print('|   ', end='')
                elif self.board_state[i][j] == 'X':
                    print('| X ', end='')
                elif self.board_state[i][j] == 'O':
                    print('| O ', end='')
                else:
                    raise ValueError("Invalid value in the board")
            print("|")
        print('-------------')

    def init_board(self):
        number_board = [[str(i+1) for i in range(j*3, (j+1)*3)] for j in range(3)]
        print("\nGame board:")
        for row in number_board:
            print('-------------')
            print('| ' + ' | '.join(row) + ' |')
        print('-------------\n')

    def empty_cells(self, state = None):
        cells = []
        if state == None:
            return self.avail_moves # Return the empty cells of current board state
            
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells
    
    def valid_move(self, x, y):
        if (x, y) in self.avail_moves:
            return True
        else:
            return False
    
    def set_move(self, x, y, player):
        if self.valid_move(x, y):
            self.board_state[x][y] = player.letter
            self.last_move = (x, y)
            self.avail_moves.remove([x, y])
            return True
        else:
            return False

    def wins(self, player, state=None):
        if state == None:
            state = self.board_state # current state
            
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    def game_over(self):
        return self.wins('X') or self.wins('O') or len(self.avail_moves) == 0
    
class Gomoku(Game):
    SIZE = 15 # Fix the the board to be 15x15
    def __init__(self):  
        self.board_state = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.avail_moves = {(i, j) for j in range(self.SIZE) for i in range(self.SIZE)}
        self.last_move = (-1, -1)

    def print_board(self):
        height = len(self.board_state)
        width = len(self.board_state[0])

        print("\n  ", end="")
        for x in range(width):
            print("{0:6d}".format(x), end='')
        print('\r\n')
        for i in range(height):
            print("{0:3d}  ".format(i), end='')
            for j in range(width):
                if self.board_state[i][j] == None:
                    print('_'.center(6), end='')
                elif self.board_state[i][j] == 'X':
                    print('X'.center(6), end='')
                elif self.board_state[i][j] == 'O':
                    print('O'.center(6), end='')
                else:
                    raise ValueError("Invalid value in the board")
            print('\n')

    def init_board(self):
        height = len(self.board_state)
        width = len(self.board_state[0])

        print("\nGame board. Type 'row,column' to select move. For example, '0,0' selects top left move.\n\n", end="  ")
        for x in range(width):
            print("{0:6d}".format(x), end='')
        print('\r\n')
        for i in range(height):
            print("{0:3d}  ".format(i), end='')
            for j in range(width):
                print('_'.center(6), end='')
            print('\n')
        print('\n')

    def empty_cells(self, state=None):
        if state is None:
            state = self.board_state  # Use current state if not provided
        cells = []
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                if state[x][y] == 0:
                    cells.append([x, y])
        return cells

    def valid_move(self, x, y):
        return 0 <= x < self.SIZE and 0 <= y < self.SIZE and self.board_state[x][y] == 0

    def set_move(self, x, y, player):
        if self.valid_move(x, y):
            self.board_state[x][y] = player.letter
            self.last_move = (x, y)
            return True
        return False

    def wins(self, player, state=None):
        # Check if the player wins in the given state, based on the last move
        if state is None:
            state = self.board_state
            
        last_x, last_y = self.last_move
        if self.last_move == (-1, -1) or state[last_x][last_y] != player.letter:
            return False
        
        # four directions: vertical, horizontal, two diagonals
        directions = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
        
        for axis in directions:
            axis_count = 1
            for (xdirection, ydirection) in axis:
                axis_count += self.direction_count(last_x, last_y, xdirection, ydirection, player, state)
                if axis_count >= 5:
                    return True
        return False
    
    def direction_count(self, x, y, xdirection, ydirection, player, state):
        # Count the number of consecutive pieces in a certain direction
        count = 0
        for step in range(1, 5):  # look four more steps on a certain direction
            if xdirection != 0 and (x + xdirection * step < 0 or x + xdirection * step >= self.SIZE):
                break
            if ydirection != 0 and (y + ydirection * step < 0 or y + ydirection * step >= self.SIZE):
                break
            if state[x + xdirection * step][y + ydirection * step] == player.letter:
                count += 1
            else:
                break
        return count 

    def game_over(self):
        # Check if the game is over (either a player wins or the board is full)
        return self.wins('X') or self.wins('O') or len(self.avail_moves) == 0
        