import calendar
import cv2
import numpy as np

# Dimensions of the grid
ROWS = 7
COLS = 7
CELL_SIZE = 20
BORDER = 0
GRID_LINE = 2
PUZZLE_HEIGHT = (BORDER * 2) + (CELL_SIZE * ROWS) + ((ROWS - 1) * GRID_LINE)
PUZZLE_WIDTH = (BORDER * 2) + (CELL_SIZE * COLS) + ((COLS - 1) * GRID_LINE)

# Colors of the grid
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [150, 150, 150]
BORDER_COLOR = [80, 80, 80]


# Parse the txt file of puzzles and return a 2d array of 0s and 1s
def read_puzzles():
    encodings = []
    with open("sevens.txt", "r") as f:
        for line in f.readlines():
            encodings.append(line.strip().replace(" ", ""))

    parsed_puzzles = []
    for e in sorted(encodings)[::-1]: # sorted!!
        array = [[0] * COLS for _ in range(ROWS)]
        for i in range(ROWS):
            for j in range(COLS):
                array[i][j] = e[(i * COLS) + j]
        parsed_puzzles.append(array)

    return parsed_puzzles


# Draw a single cell of the puzzle
def draw_cell(color):
    cell = np.zeros((CELL_SIZE, CELL_SIZE, 3), dtype=np.uint)
    cell[:, :] = color
    return cell


# Draw a puzzle with the specified sizes and colors
def draw_puzzle(p):

    # Initialize the blank image
    image = np.zeros((PUZZLE_HEIGHT, PUZZLE_WIDTH, 3), dtype=np.uint8)
    image[:, :] = BORDER_COLOR

    # Fill in each cell of the puzzle
    for r in range(ROWS):
        for c in range(COLS):
            color = BLACK if p[r][c] == "1" else WHITE
            cell = draw_cell(color)
            r_start = BORDER + (CELL_SIZE * r) + (r * GRID_LINE)
            r_stop = r_start + CELL_SIZE
            c_start = BORDER + (CELL_SIZE * c) + (c * GRID_LINE)
            c_stop = c_start + CELL_SIZE
            image[r_start:r_stop, c_start:c_stop] = cell

    return image

if __name__ == "__main__":

    # Figure out the dates
    cal = calendar.Calendar(4) # 2021 starts on a Friday
    dates, seen = [], set()
    for i in range(1, 13):
        for e in cal.itermonthdates(2021, i):
            month_day = str(e)[5:]
            if month_day not in seen:
                dates.append(month_day)
                seen.add(month_day)

    # Filter the dates to remove Saturdays
    relevant_dates = [e for i, e in enumerate(dates) if (i + 4) % 7 != 0]

    # Draw and save the puzzles
    ps = read_puzzles()
    for i, p in enumerate(ps):
        date = relevant_dates[i]
        file_name = "puzzle_images/{}.jpg".format(date)
        pic = draw_puzzle(p)
        cv2.imwrite(file_name, pic)

    # Print out the accompanying html
    for e in relevant_dates:
        print('  <div class="column">')
        print('    <img src="data/puzzle_images/{}.png" title="{}">'.format(e, e))
        print('  </div>')