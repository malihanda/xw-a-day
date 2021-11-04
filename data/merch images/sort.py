import cv2
import os


# list of (file name, pigmentation) tuples
pixels = []

for file in os.listdir():
    if not file.endswith("png"):
        continue

    pigmentation = cv2.imread(file).sum()
    print(pigmentation)
    pixels.append((file, pigmentation))

# sort the list so that the most pigmented are at the beginning
pixels.sort(key = lambda x: x[0])
pixels.sort(key = lambda x: x[1])

# rename the files so they are sorted
count = 10
for file, _ in pixels:
    image = cv2.imread(file)
    new_path = "sorted/" + str(count) + ".png"
    cv2.imwrite(new_path, image)
    count += 1


