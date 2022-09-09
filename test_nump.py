import numpy as np

arr = np.array([[0, 0], [0, 1], [0, 2], [0, 3]])

arr[:, 1] += 2

print(arr)