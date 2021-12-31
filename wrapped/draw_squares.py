import cv2
import numpy as np


# Dimensions of the image
ROWS = 91
COLS = 168
CELL_SIZE = 20
BORDER = 10
GRID_LINE = 10
IMAGE_HEIGHT = (BORDER * 2) + (CELL_SIZE * ROWS) +  ((ROWS - 1) * GRID_LINE)
IMAGE_WIDTH = (BORDER * 2) + (CELL_SIZE * COLS) +  ((COLS - 1) * GRID_LINE)


# Colors of the image
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
BORDER_COLOR = [179, 179, 179]


# Draw a single square
def draw_cell(color, number):
    size = CELL_SIZE
    cell = np.zeros((size, size, 3), dtype=np.uint)
    cell[:, :] = color
    return cell


# Draw a the squares
def draw_squares():

    # Initialize the blank image
    image = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
    image[:, :] = BORDER_COLOR

    # Fill in each square
    count = 0
    for r in range(ROWS):
        for c in range(COLS):
            count +=1 
            color = BLACK if count < 3950 else WHITE

            cell = draw_cell(color, (COLS) + c)
            r_start = BORDER + (CELL_SIZE * r) + (r * GRID_LINE)
            r_stop = r_start + CELL_SIZE
            c_start = BORDER + (CELL_SIZE * c) + (c * GRID_LINE)
            c_stop = c_start + CELL_SIZE
            image[r_start:r_stop, c_start:c_stop] = cell

    return image

sq = draw_squares()
cv2.imwrite("data/squares.png", sq)