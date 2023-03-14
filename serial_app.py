
import math
import numpy as np
import pandas as pd

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
        x = np.random.random() * width
        y = np.random.random() * height

        left = x - radius
        right = x + radius
        bottom = y - radius
        top = y + radius
        # Check if the circle is fully in the box
        if left > 0 and right < width and bottom > 0 and top < height:
            # Check if the circle is overlapping another circle
            overlapping = False
            for i in range(len(x_coordinates)):
                x_to_check = x_coordinates[i]
                y_to_check = y_coordinates[i]
                distance_between_circles = 0.5 * ((x_to_check - x)**2 + (y_to_check - y)**2)
                if distance_between_circles < 2 * radius:
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
    
    pd.DataFrame({"Number of Samples": pd.Series(samples), "Packing Fraction": pd.Series(PFs)}).to_csv("PF_vs_samples.csv", index=False)
        

