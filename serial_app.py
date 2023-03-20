
import math
import numpy as np
import pandas as pd

from plot_data import plot
from utils import circles_are_overlapping

def main(width, height, radius, num_of_samples):
    """
    Calculates the packing fraction vs number of samples for a 2D box containing random samples of circles
    """
    # Constants
    pi = 3.141592653589793238
    circle_area = pi * (radius ** 2)
    box_area = width * height

    # Data
    x_coordinates = []
    y_coordinates = []
    PFs = [0]
    samples = [0]

    for sample_number in range(num_of_samples):
        # Generate random coordinate 
        x = radius + np.random.random() * (width - radius * 2)
        y = radius + np.random.random() * (height - radius * 2)

        # Check if the circle is overlapping another circle
        overlapping = False
        for i in range(len(x_coordinates)):
            x_to_check = x_coordinates[i]
            y_to_check = y_coordinates[i]
            if circles_are_overlapping(x, y, x_to_check, y_to_check, radius):
                overlapping = True
                break

        if not overlapping:
            x_coordinates.append(x)
            y_coordinates.append(y)

        # Save data point
        num_of_circles = len(x_coordinates)
        if sample_number % math.floor(num_of_samples * 0.01) == 0:
            packing_fraction = (num_of_circles * circle_area) / box_area
            print(f"Packing fraction for {sample_number} samples and {num_of_circles} circles is {packing_fraction}")
            PFs.append(packing_fraction)
            samples.append(sample_number)
    
    samples_vs_PF_DF = pd.DataFrame({"Number of Samples": pd.Series(samples), "Packing Fraction": pd.Series(PFs)})
    coordinates_DF = pd.DataFrame({"x": pd.Series(x_coordinates), "y": pd.Series(y_coordinates), "rank": pd.Series(np.zeros((len(x_coordinates))))})

    plot(width, height, radius, samples_vs_PF_DF, coordinates_DF)
    

