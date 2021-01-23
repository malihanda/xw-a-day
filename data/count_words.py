import os
import puz


# Store words in a string --> int dictionary
counts = dict()

# .puz files are stored in puz_files/mm/mm-dd.puz files
folders = os.listdir("puz_files")
for f in folders:

    # Ignore the drafts and the non-7x7s
    if f in ["drafts", "other-puzzles"]:
        continue

    puzs = os.listdir("puz_files/" + f)

    for p in puzs:
        puzzle_path = "/".join(["puz_files", f, p])
        puzzle = puz.read(puzzle_path)
        n = puzzle.clue_numbering()

        # Across
        for clue in n.across:
            answer = "".join(puzzle.solution[clue["cell"] + i] for i in range(clue["len"]))
            if answer in counts:
                counts[answer].append(p)
            else:
                counts[answer] = [p]

        # Down
        for clue in n.down:
            answer = "".join(puzzle.solution[clue["cell"] + i * n.width] for i in range(clue["len"]))
            if answer in counts:
                counts[answer].append(p)
            else:
                counts[answer] = [p]


for w, i in counts.items():
    if len(i) != 1:
        if i[1] < "01-24.puz":
            print(w, i)
