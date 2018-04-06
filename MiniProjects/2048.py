#! python2
"""
Clone of 2048 game.
"""

import random
import poc_2048_gui
import user44_Ut2BopgRTT_7 as ts
import user44_nqvQ4mtOMD_1 as ts2

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    final_len = len(line)
    condensed_list = list(filter(lambda num: num > 0, line))
    return_line = squish(condensed_list, 0)
    while len(return_line) < final_len:
        return_line += [0]
    return return_line

def squish(condensed_list, start):
    """
    Function that merges adjacent same numbers from the left.
    """
    squished = list(condensed_list)
    for idx, num in enumerate(condensed_list):
        if idx < start:					# not at start
            continue
        elif idx >= len(squished) - 1:	# at end
            return squished
        elif num == squished[idx + 1]:	# squish
            squished[idx] += squished.pop(idx + 1)
            return squish(squished, idx + 1)
    return squished

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self.initial_dict()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)]\
                      for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return '\n'.join(map(str, [row for row in self._grid]))

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initial_state = self.__str__()
        seeds = self._initial_dict[direction]
        stopper = self._height if direction < 2.5 else self._width

        for seed in seeds:
            indicies = self.index_list(seed, OFFSETS[direction], stopper)
            values = [self.get_tile(row, col) for row, col in indicies]
            moved_values = merge(values)
            for idx in range(stopper):
                self.set_tile(indicies[idx][0], indicies[idx][1], moved_values[idx])
        new_state = self.__str__()

        if new_state != initial_state:
            self.new_tile()
        else:
            print 'No move ', direction

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.random() < 0.9:
            new_val = 2
        else:
            new_val = 4

        empty = False
        while not empty:
            row = random.randrange(self._height)
            col = random.randrange(self._width)
            if self.get_tile(row, col) == 0:
                empty = True
        else:
            self.set_tile(row, col, new_val)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def initial_dict(self):
        """
        Create a dictionary with initial 'seed' indicies for the first
        index of each row/col associated with a given merge direction.
        """
        self._initial_dict = {
            UP: [(0, col) for col in range(self._width)],
            DOWN: [(self._height - 1, col) for col in range(self._width)],
            LEFT: [(row, 0) for row in range(self._height)],
            RIGHT: [(row, self._width - 1) for row in range(self._height)],
            }

    def index_list(self, seed, offset, stop):
        '''
        Return a list of indicies of row/col.
        Given the initial index, offset/step, and # of iterations
        '''
        return [self.row_col_add(seed, offset, index)for index in range(stop)]

    def row_col_add(self, row_col_root, row_col_offset, multiplier=1):
        """
        Add together two row/column tuple pairs.
        Additional argument can be used to multiply the offset tuple values.
        """
        return (row_col_root[0] + row_col_offset[0] * multiplier,\
                row_col_root[1] + row_col_offset[1] * multiplier)



#ts.run_suite(TwentyFortyEight)
#ts2.run_suite(TwentyFortyEight)
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
