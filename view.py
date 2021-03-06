import tkinter as tk
import numpy as np
from functools import partial
from model import GameOverError, TileFlippedError, TileOutOfBoundsError

class View(tk.Tk):
    def __init__(self, model):
        super().__init__()

        # Bind keyboard controller
        self.bind("<Key>", self.handle_keypress)

        self.model = model
        self.length, self.width = self.model.board.shape

        # Title
        title_frm = tk.Frame(master=self)
        title_frm.pack()
        title_lbl = tk.Label(text="Voltorb Flip", width=40, master=title_frm)
        title_lbl.pack(fill=tk.X, side=tk.TOP)

        # Board
        board_frm = tk.Frame(master=self)
        board_frm.pack()

        # Grid of Buttons - A 2D array that stores all the buttons.
        self.button_array = np.full((self.length, self.width),
                                     None,
                                     dtype=tk.Button)

        for i, row in enumerate(model.board):
            for j, tile in enumerate(row):
                grid_frm = tk.Frame(master=board_frm)
                grid_frm.grid(row=i, column=j)

                btn_callback = partial(self.flip_tile, i, j)

                grid_btn = tk.Button(text="?",
                                     height=3,
                                     width=5,
                                     master=grid_frm,
                                     command=btn_callback)
                grid_btn.pack()

                self.button_array[i][j] = grid_btn

            # At the end of every row, add the row information
            sum_score, voltorbs = self.model.row_data[i]
            row_lbl = tk.Label(text=f"{sum_score} {voltorbs}V",
                               width=5,
                               master=board_frm)
            row_lbl.grid(row=i, column=self.model.width+1)

        # At the bottom, add all the column information
        for j in range(len(self.model.col_data)):
            sum_score, voltorbs = self.model.col_data[j]
            col_lbl = tk.Label(text=f"{sum_score} {voltorbs}V",
                               width=5,
                               master=board_frm)
            col_lbl.grid(row=self.model.length+1, column=j)

        # Score indicator
        score_frm = tk.Frame(master=self)
        score_frm.pack()
        self.score_lbl = tk.Label(text=f"Score: 0",
                                  width=40,
                                  master=score_frm)
        self.score_lbl.pack(fill=tk.X, side=tk.TOP)

        # Error indicator
        error_frm = tk.Frame(master=self)
        error_frm.pack()
        self.error_lbl = tk.Label(text="", width=40, master=error_frm)
        self.error_lbl.pack(fill=tk.X, side=tk.TOP)

    def flip_tile(self, i, j):
        """
        Callback function for Tkinter to update the state of the game
        and change the view of the buttons and score.
        """
        # Flip the tile in the model
        try:
            self.model.flip_tile(i, j)
        except GameOverError:
            self.error_lbl["text"] = "The game has ended."
        except TileFlippedError:
            self.error_lbl["text"] = "This tile has already been flipped."
        except TileOutOfBoundsError:
            raise IndexError("Bad tile indices.")
        else:
            self.error_lbl["text"] = ""
        # Update the tile's text
        self.button_array[i][j]["text"] = self.model.describe_tile(i, j)
        # Update the score indicator
        self.score_lbl["text"] = f"Score: {self.model.score}"


    def handle_keypress(self, event):
        if event.char == 'q':
            self.destroy()
