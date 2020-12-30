"""
Contains the model of the voltorb-flip game. Handles generation of board,
flipping mechanisms, game over, and points earned.
"""
import math
import random

def reshape2D(array, length, width):
    """
    Reshapes a 1D Python list into a 2D one.
    """
    # Make sure there's enough elements
    assert len(array) == length * width

    reshaped = [array[n:(n + length)] for n in range(0, len(array), length)]

    return reshaped

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

def generate_board(length, width, difficulty):
    """
    Takes a length and a width. Returns a 2D list that contains
    0 for a voltorb, and 1/2/3 for their respective values.
    """
    total_tiles = length * width
    tile_distribution = difficulty_to_tile_distribution(length, width, difficulty)

    board = []

    for i, num_tiles in enumerate(tile_distribution):
        board.extend([i] * num_tiles)

    random.shuffle(board)

    return reshape2D(board, length, width)

def get_row_data(board):
    """
    Returns a list of tuples that contain the
    total sum of the numbers in the row
     and the number of voltorbs in a row
    """
    row_data = []

    for row in board:
        row_data.append(tuple([sum(row), row.count(0)]))

    return row_data

def get_col_data(board):
    """
    Returns a list of tuples that contain the
    total sum of the nubmers in the row
    and the number of voltorbs in a column
    """
    col_data = []

    for col_num in range(len(board)):
        # pretty inefficient to recreate columns, probably should use numpy
        # arrays...
        col = [board[row_num][col_num] for row_num in range(len(board[0]))]
        col_data.append(tuple([sum(col), col.count(0)]))

    return col_data

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
        self.board = generate_board(length, width, difficulty)

        total_tiles = length * width
        self.flipped = reshape2D([False] * total_tiles, length, width)

        self.row_data = get_row_data(self.board)
        self.col_data = get_col_data(self.board)

        self.score = 0
        self.game_over = False

    def flip_tile(self, row, col):
        """
        Flips over the tile in the specified, zero-indexed, row and column.

        Manages exceptions for flipping an already flipped tile,
        game over, and points earned when you flip.
        """
        if row >= self.length or row < 0 or col >= self.width or col < 0:
            raise Exception("Played in a tile that does not exist on the board.")

        if self.flipped[row][col]:
            raise Exception("This tile has already been flipped!")

        if self.game_over:
            raise Exception("The game is over, you already lost!")

        flipped_tile_value = self.board[row][col]
        self.flipped[row][col] = True

        if flipped_tile_value == 0:
            self.game_over = True

        if self.score == 0:
            if self.game_over:
                self.score = "YOU LOSE"
            else:
                self.score = flipped_tile_value
        else:
            self.score *= flipped_tile_value

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
