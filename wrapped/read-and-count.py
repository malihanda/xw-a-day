# nothing in this file is fast, or optimized. it doesn't need to be, because
# everything is O(312), that is, O(1)
# or whatever

from collections import Counter
import os
import puz as puzpy
import string


# utility function for debugging
def print_puzzle(p):
    for row in p:
        r = row.replace("1", "# ")
        r = r.replace("0", "- ")
        print(r)
    return


# the puzzles are stored as 1s and 0s
# rows are separated by spaces; puzzles are separated by \n's
puzzles = []
with open("data/sevens.txt") as f:
    for line in f.readlines():
        puz = line.strip().split(" ")
        puzzles.append(puz)


# count the black squares total
black_squares = 0
for puz in puzzles:
    for row in puz:
        for c in row:
            black_squares += (c == "1")
# print("black squares:", black_squares)


# count the black squares per puzzle
counts = []
for puz in puzzles:
    black_squares = 0
    for row in puz:
        for c in row:
            black_squares += (c == "1")
    counts.append(black_squares)

collected = Counter(counts)
# print("\nblack squares per puzzle:")
# for item in collected.items():
#     print(item)

with open("data/black_squares_each.csv", "w") as f:
    output = "\n".join(["squares"] + [str(c) for c in counts])
    f.write(output)


# count the words in each puzzle
# a puzzle can either have one or two words in a row / col
def one_or_two(line):
    if line == "0001000":
        return 2
    else:
        return 1

def count_words(p):
    c = 0
    for row in p:
        c += one_or_two(row)
    for i in range(7):
        col = "".join([r[i] for r in p])
        c += one_or_two(col)
    return c

counts = [count_words(puz) for puz in puzzles]
collected = Counter(counts)
# print("\nnumber of words:")
for item in collected.items():
    # print(item)
    continue


# count the words total
# a puzzle can either have one or two words in a row / col
def word_lengths(line):
    if line == "0001000":
        return [3, 3]
    else:
        return [len(line.replace("1", ""))]

counts = []
for puz in puzzles:
    for row in puz:
        counts.extend(word_lengths(row))
    for i in range(7):
        col = "".join([row[i] for row in puz])
        counts.extend(word_lengths(col))

collected = Counter(counts)
# print("\ntotal words:", len(counts))
# print("number of words of length n:")
for item in collected.items():
    # print(item)
    continue

with open("data/entry_lengths.csv", "w") as f:
    output = "\n".join(["len"] + [str(c) for c in counts])
    f.write(output)


# parse all of the puzzles to get the fill and the clues
entries = dict()  # entry -> list of clues

def parse_puzzle(p, d):
    num = p.clue_numbering()

    # across entries
    for c in num.across:
        entry = "".join(p.solution[c["cell"] + i] for i in range(c["len"]))
        if entry in d:
            d[entry].append(c["clue"].lower())
        else:
            d[entry] = [c["clue"].lower()]

    # down entries
    for c in num.down:
        entry = "".join(p.solution[c["cell"] + i * num.width] for i in range(c["len"]))
        if entry in d:
            d[entry].append(c["clue"].lower())
        else:
            d[entry] = [c["clue"].lower()]

    return

folders = [f"../data/puz_files/{i:02d}" for i in range(1, 13)]
for f in folders:
    for puz_path in os.listdir(f):
        path = f + "/" + puz_path
        p = puzpy.read(path)
        parse_puzzle(p, entries)


# print("\nn unique entries:", len(entries))


# how many unique entries were there for each number of letters?
# print("\nentries for each word length:")
# print("(# letters, # entries, # unique, pct unique)")
for i in range(3, 8):
    relevant = [(e, clues) for e, clues in entries.items() if len(e) == i]
    n_unique = len(relevant)
    n_entries = sum([len(cs) for e, cs in relevant])
    # print(i, n_entries, n_unique, n_unique / n_entries)


# what were the three letter words?
tlw = [e for e in entries if len(e) == 3]
tlw.sort()
with open("data/tlw.txt", "w") as f:
    text = " ".join(tlw)
    f.write(text)


# what are the most common entries of each length?
# print("\nmost common entries:")
common_entries = []
for i in range(3, 8):
    relevant_entries = [(k, v) for k, v in entries.items() if len(k) == i]
    most = max([len(v) for k, v in relevant_entries])
    top_fill = [k for k, v in relevant_entries if len(v) == most]
    # print("length:", i, "count:", most)
    # print(sorted(top_fill))


# make a txt of all the entries used, for word cloud purposes
all_entries = []
for e, cs in entries.items():
    all_entries.append(e + "," + str(len(cs)))

with open("data/entries.csv", "w") as f:
    text = "\n".join(["entry,n"] + all_entries)
    f.write(text)


# lets look at letter distributions
def clean(txt):
    with open(txt, encoding="utf8") as f:
        text = f.read().upper()

    letters = [c for c in text if c.isalpha()]
    return Counter(letters)

letters_wiki = clean("data/wikipedia.txt")
count_wiki = sum([n for l, n in letters_wiki.items()])
letters_xw = clean("data/entries.csv")
count_xw = sum([n for l, n in letters_xw.items()])
lines = ["letter,type,prop"]
for c in string.ascii_uppercase:
    lines.append(c + ",xw," + str(letters_xw[c] / count_xw))
    lines.append(c + ",wiki," + str(letters_wiki[c] / count_wiki))
with open("data/letter_dist.csv", "w") as f:
    text = "\n".join(lines)
    f.write(text) 


# which was the longest clue?
longest = 0
best_word = None
best_clue = None
for word, clues in entries.items():
    for clue in clues:
        if len(clue) > longest:
            longest = len(clue)
            best_word = word
            best_clue = clue
# print("\nthe longest clue was", longest, "characters:", best_clue, "for", best_word)


# get the names of unique constructors using a bit of gross text searching
with open("data/index.txt") as f:
    named_lines = []
    for line in f.readlines():
        if "claimed by" in line:
            line = line.replace("claimed by", "")
        if "(" in line:
            first_half = line.split("(")[1]
            name = first_half.split(")")[0]
            named_lines.append(name.strip())

all_names = []
collabs = 0
for name in named_lines:
    if "+" in name:
        collabs += 1
        collab = name.split(" + ")
        all_names.extend(collab)
    else:
        all_names.append(name)

collected = Counter(all_names)
# print("\ntop contributors:")
top = [(name, n) for name, n in collected.items() if n >= 4]
top.sort(key = lambda x: -x[1])
for item in top:
    # print(item)
    continue
# print("\nnumber of collaborations:", collabs)
# print("number of constructors:", len(collected))


# get the first names
first_names = dict()
for name, count in collected.items():
    first_name = name.split(" ")[0]
    if first_name in first_names:
        first_names[first_name].append((name, count))
    else:
        first_names[first_name] = [(name, count)]
# print("number of first names:", len(first_names))

multiples = []
unique = 0
for first, num in first_names.items():
    if len(num) != 1:
        multiples.append((first, len(num), sum(n for _, n in num)))
    else:
        unique += 1
multiples.sort(key = lambda x: -x[2])
multiples.sort(key = lambda x: -x[1])
# print("number of constructors with only their first name:", unique)


# how many puzzles each?
collected = Counter([count for name, count in Counter(all_names).items()])
# print("\nhow many constructors made n puzzles?")
for e in collected.most_common():
    # print(e)
    continue





