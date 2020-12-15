import cv2
import numpy as np
import puz
import sys

# Dimensions of the grid
SIZES = {
    "ROWS": None,
    "COLS": None,
    "CELL_SIZE": 20,
    "BORDER": 0,
    "GRID_LINE": 2,
    "PUZZLE_HEIGHT": None,
    "PUZZLE_WIDTH": None, 
}

# Colors of the grid
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [150, 150, 150]
BORDER_COLOR = [80, 80, 80]


# Parse the puz file and return a 2d array of Xs and .s
def read_puzzle():
    array = [[0] * SIZES["COLS"] for _ in range(SIZES["ROWS"])]
    for i in range(SIZES["ROWS"]):
        for j in range(SIZES["COLS"]):
            array[i][j] = PUZZLE.solution[(i * SIZES["COLS"]) + j]

    return array


# Draw a single cell of the puzzle
def draw_cell(color):
    cell = np.zeros((SIZES["CELL_SIZE"], SIZES["CELL_SIZE"], 3), dtype=np.uint)
    cell[:, :] = color
    return cell


# Draw a puzzle with the specified sizes and colors
def draw_puzzle(p):

    # Initialize the blank image
    image = np.zeros((SIZES["PUZZLE_HEIGHT"], SIZES["PUZZLE_WIDTH"], 3), dtype=np.uint8)
    image[:, :] = BORDER_COLOR

    # Fill in each cell of the puzzle
    for r in range(SIZES["ROWS"]):
        for c in range(SIZES["COLS"]):
            color = BLACK if p[r][c] == "." else WHITE
            cell = draw_cell(color)
            r_start = SIZES["BORDER"] + (SIZES["CELL_SIZE"] * r) + (r * SIZES["GRID_LINE"])
            r_stop = r_start + SIZES["CELL_SIZE"]
            c_start = SIZES["BORDER"] + (SIZES["CELL_SIZE"] * c) + (c * SIZES["GRID_LINE"])
            c_stop = c_start + SIZES["CELL_SIZE"]
            image[r_start:r_stop, c_start:c_stop] = cell

    return image

if __name__ == "__main__":
    FILE_PATH = sys.argv[1]
    PUZ_FILE = "puz_files/{}.puz".format(FILE_PATH)
    IMAGE_FILE = "puzzle_images/{}.png".format(FILE_PATH)
    PUZZLE = puz.read(PUZ_FILE)

    # Assign sizes based on the puz file
    SIZES["ROWS"] = PUZZLE.height
    SIZES["COLS"] = PUZZLE.width
    SIZES["PUZZLE_HEIGHT"] = (
        (SIZES["BORDER"] * 2) + 
        (SIZES["CELL_SIZE"] * SIZES["ROWS"]) + 
        ((SIZES["ROWS"] - 1) * SIZES["GRID_LINE"]))
    SIZES["PUZZLE_WIDTH"] = (
        (SIZES["BORDER"] * 2) + 
        (SIZES["CELL_SIZE"] * SIZES["COLS"]) + 
        ((SIZES["COLS"] - 1) * SIZES["GRID_LINE"]))

    # Compute and save the image
    p = read_puzzle()
    pic = draw_puzzle(p)
    cv2.imwrite(IMAGE_FILE, pic)