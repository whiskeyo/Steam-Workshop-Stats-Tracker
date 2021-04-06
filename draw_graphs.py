import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def draw_graph(filename):
    i  = 0
    x  = [0]
    y1 = [0]
    y2 = [0]
    y3 = [0]

    print(filename)
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=";")

        i = 0
        for row in reader:
            x.append(i)
            y1.append(int(row[1]))
            y2.append(int(row[2]))
            y3.append(int(row[3]))

            i += 1

        cumulativey1 = np.cumsum(y1)
        cumulativey2 = np.cumsum(y2)
        cumulativey3 = np.cumsum(y3)

        plt.plot(x, cumulativey1, label="New visitors")
        plt.plot(x, cumulativey2, label="New subscribers")
        plt.plot(x, cumulativey3, label="New favorites")
        plt.show()     

# for filename in os.listdir('.'):
#     if filename.endswith(".txt"):
#         draw_graph(filename)

draw_graph("05-04-2021.txt")