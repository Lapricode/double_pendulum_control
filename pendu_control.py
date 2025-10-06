import numpy as np
from pendu_visualization import animate_system


states = []
for i in range(1000):
    states.append(np.array([[0.], [0.]]))

animate_system(states, 1, 0.1, 1, 1)