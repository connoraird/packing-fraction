
import math
import numpy as np
import pandas as pd

from plot_data import plot
from utils import new_circle_is_overlapping_existing_circles

def main(width, height, radius, num_of_samples):
    """
    Calculates the packing fraction (PF) for a 2D box containing random samples of circles and plots PF against samples.

    :param float width: The width of the 2D box
    :param float heigh: The height of the 2D box
    :param float radius: the radius of circles to fill the box with
    :param float num_of_samples: The total number of sample cirles to attempt to fit into the box 
    
    :return: the packing fraction
    """
    # Constants
    pi = 3.141592653589793238
    diameter = 2*radius
    circle_area = pi * (radius ** 2)
    box_area = width * height
    batch_size = math.floor(num_of_samples * 0.01)

    # Data
    coordinates = []
    PFs = [0]
    samples = [0]

    for sample_number in range(num_of_samples):
        # Generate random coordinate 
        x = radius + np.random.random() * (width - diameter)
        y = radius + np.random.random() * (height - diameter)

        if not new_circle_is_overlapping_existing_circles(x, y, coordinates, diameter):
            coordinates.append([x,y])

        # Save data point
        num_of_circles = len(coordinates)
        if sample_number % batch_size == 0 or sample_number == num_of_samples - 1:
            packing_fraction = (num_of_circles * circle_area) / box_area
            print(f"Packing fraction for {sample_number} samples and {num_of_circles} circles is {packing_fraction}")
            PFs.append(packing_fraction)
            samples.append(sample_number)
    
    samples_vs_PF_DF = pd.DataFrame({"Number of Samples": pd.Series(samples), "Packing Fraction": pd.Series(PFs)})
    coordinates_DF = pd.DataFrame({"x": pd.Series([coord[0] for coord in coordinates]), "y": pd.Series([coord[1] for coord in coordinates]), "rank": pd.Series(np.zeros((len(coordinates))))})

    plot(width, height, radius, samples_vs_PF_DF, coordinates_DF)

    return packing_fraction
    