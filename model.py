"""
Contains the model of the voltorb-flip game. Handles generation of board,
flipping mechanisms, game over, and points earned.
"""
import math
import random
import numpy as np

class GameOverError(Exception):
    pass

class TileFlippedError(Exception):
    pass

class TileOutOfBoundsError(Exception):
    pass


def difficulty_to_tile_distribution(length, width, difficulty):
    """
    Takes a positive integer greater than 1 for difficulty. Returns the
    [number of voltorbs, number of 1 tiles, number of 2 tiles,
    number of 3 tiles] as an array of length 4.

    The higher the difficulty, the more 3 tiles and the more voltorbs.
    """
    total_tiles = length * width
    tile_distribution = [0, 0, 0, 0]

    tile_distribution[0] = math.floor(total_tiles * 0.3 + difficulty * 0.5)
    tile_distribution[1] = math.floor(total_tiles * 3 / 4) - tile_distribution[0]

    num_multiplier_tiles = total_tiles - math.floor(total_tiles * 3 / 4)
    low_bound_two_tiles = max(0, num_multiplier_tiles - difficulty)

    tile_distribution[2] = random.randint(low_bound_two_tiles, num_multiplier_tiles)
    tile_distribution[3] = num_multiplier_tiles - tile_distribution[2]

    return tile_distribution

def generate_board(length, width, tile_distribution):
    """
    Takes a length, width, and tile distribution. Returns a 2D numpy array
    that contains 0 for a voltorb, and 1/2/3 for their respective values.
    """
    board = []

    for i, num_tiles in enumerate(tile_distribution):
        board.extend([i] * num_tiles)

    random.shuffle(board)

    return np.reshape(np.array(board), (length, width))

def get_row_col_data(board, axis):
    """
    Returns a list of tuples that contain the
    total sum of the nubmers in the row
    and the number of voltorbs in the correct axis, where
    0 is for the columns and 1 is the rows.
    """
    col_sums = board.sum(axis=axis)
    col_voltorbs = (board == 0).sum(axis=axis)

    return list(zip(col_sums, col_voltorbs))

def board_to_string(board):
    s = ""

    for row in board:
        for el in row:
            s += str(el)
            s += "|"
        s += "\n"

    return s

class Model:
    def __init__(self, length, width, difficulty):
        self.length = length
        self.width = width
        self.difficulty = difficulty
        self.tile_distribution = difficulty_to_tile_distribution(length, width, difficulty)
        # A better way to do this would be with logical indexing and numpy arrays...
        # let's do that instead.
        #self.multiplier_tiles = self.tile_distribution[2] + self.tile_distribution[3]
        self.board = generate_board(length, width, self.tile_distribution)

        total_tiles = length * width
        self.flipped = np.full((length, width), False)

        self.row_data = get_row_col_data(self.board, 1)
        self.col_data = get_row_col_data(self.board, 0)

        self.score = 0
        self.game_over = False

    def flip_tile(self, row, col):
        """
        Flips over the tile in the specified, zero-indexed, row and column.

        Manages exceptions for flipping an already flipped tile,
        game over, and points earned when you flip.
        """
        if row >= self.length or row < 0 or col >= self.width or col < 0:
            raise TileOutOfBoundsError

        if self.flipped[row][col]:
            raise TileFlippedError

        if self.game_over:
            raise GameOverError

        flipped_tile_value = self.board[row][col]
        self.flipped[row][col] = True

        remaining_tiles = self.board[~self.flipped]
        twos_threes_remaining = 2 in remaining_tiles or 3 in remaining_tiles

        if flipped_tile_value == 0:
            self.score = "YOU LOSE"
            self.game_over = True
        elif self.score == 0:
            self.score = flipped_tile_value
        else:
            self.score *= flipped_tile_value
            if not twos_threes_remaining:
                self.score = "YOU WON"
                self.game_over = True

    def describe_tile(self, row, col):
        """
        Returns a string that gives information about what value the tile
        has based on whether it's flipped or not. An "?" signifies
        a tile that has not been flipped.
        """
        if not self.flipped[row][col]:
            return "?"
        else:
            return str(self.board[row][col])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = "Board:\n"
        s += board_to_string(self.board)
        s += "Flipped:\n"
        s += board_to_string(self.flipped)

        s += ("Row Data: " + str(self.row_data) + "\n")
        s += ("Col Data: " + str(self.col_data) + "\n")

        return s
