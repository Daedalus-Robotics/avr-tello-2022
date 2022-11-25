from resources.tellopic import MissionPad
import numpy as np

textron = np.ndarray(shape=(2, 4), dtype=MissionPad)

pads = np.array([7, 1, 3, 5, 8, 2, 4, 6]).reshape(2, 4)

print(pads)

for row in range(2):
    for col in range(4):
        textron[row, col] = MissionPad(pads[row, col], False)
        # print(textron[row, col].get_pad())

print(np.where(pads == 7))
print(pads[np.where(pads == 7)])
