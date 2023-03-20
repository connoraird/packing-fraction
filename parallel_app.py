
import numpy as np
import pandas as pd
from mpi4py import MPI
import math

from plot_data import plot
from utils import circles_are_overlapping
from utils import get_overlapping_circles

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
    circle_area = pi * (radius ** 2)
    box_area = width * height

    # Processor info 
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_processors = comm.Get_size()
    if num_processors % 2 != 0 or num_processors > 1000:
        raise Exception(f"Must be ran with an even number of processors less than 1000, given: {num_processors}")
    num_samples_per_processor = math.floor(num_of_samples / num_processors)
    section_width = width * 0.5
    section_height = 2 * (height / num_processors)
    section_x_0 = (rank % 2) * section_width
    section_y_0 = section_height * math.floor(rank * 0.5)
    send_right_message_tag = rank + 1000
    receive_right_message_tag = rank - 1 + 1000
    send_up_message_tag = rank + 2000
    receive_up_message_tag = rank - 2 + 2000
    on_left = (rank % 2) == 0
    on_right = not on_left
    on_bottom = rank < 2
    on_top = rank > num_processors - 3
    send_veritcal_traffic = num_processors > 2

    # Data
    coordinates_for_one_processor = []
    central_coordinates = []
    right_edge = []
    left_edge = []
    top_edge = []
    bottom_edge = []
    packing_fractions = [0]
    samples = [0]

    for sample_number in range(num_samples_per_processor):
        # Create a data point if this is not the first sample and either we are at the last sample or we have done a 100th of the total samples
        should_create_data_point = sample_number > 0 and (sample_number == num_samples_per_processor - 1 or (sample_number % math.floor(num_samples_per_processor * 0.01)) == 0)
        if should_create_data_point:
            comm.barrier()
            if on_left:
                right_halo_req = comm.isend(right_edge, dest=rank + 1, tag=send_right_message_tag)
            else:
                left_halo_rec = comm.irecv(source=rank - 1, tag=receive_right_message_tag)
            if send_veritcal_traffic:
                if not on_top:
                    top_halo_req = comm.isend(top_edge, dest=rank + 2, tag=send_up_message_tag)
                if not on_bottom:
                    bottom_halo_rec = comm.irecv(source=rank - 2, tag=receive_up_message_tag)
        
        # Generate random coordinate 
        x = section_x_0 + np.random.random() * section_width 
        y = section_y_0 + np.random.random() * section_height

        # Check if the circle is fully in the box
        overlapping = False
        if on_left:
            if x < radius:
                overlapping = True
        else:
            if x > width - radius:
                overlapping = True
        if on_bottom:
            if y < radius:
                overlapping = True
        if on_top:
            if y > height - radius:
                overlapping = True
                
        # Check if the circle is overlapping another circle within the section
        coordinates_for_one_processor = central_coordinates + right_edge + left_edge + top_edge + bottom_edge
        for coordinate in coordinates_for_one_processor:
            x_to_check = coordinate[0]
            y_to_check = coordinate[1]
            if circles_are_overlapping(x, y, x_to_check, y_to_check, radius):
                overlapping = True
                break
        
        # Check if the circle is in an edge region
        if not overlapping:
            in_halo = False
            if x > section_x_0 + section_width - radius:
                in_halo = True
                right_edge.append([x, y])
            elif x < section_x_0 + radius:
                in_halo = True
                left_edge.append([x, y])
            
            if y > section_y_0 + section_height - radius:
                in_halo = True
                top_edge.append([x,y])
            elif y < section_y_0 + radius:
                in_halo = True
                bottom_edge.append([x, y])
            
            if not in_halo:
                central_coordinates.append([x,y])

        if should_create_data_point:
            # Remove overlapping circles in different boxes
            if on_right:
                received_left_halo = left_halo_rec.wait()
                left_circles_to_remove = get_overlapping_circles(received_left_halo, left_edge, radius)
                for circle in left_circles_to_remove:
                    left_edge.remove(circle)
            
            if send_veritcal_traffic and not on_bottom:
                received_bottom_halo = bottom_halo_rec.wait()
                bottom_circles_to_remove = get_overlapping_circles(received_bottom_halo, bottom_edge, radius)
                for circle in bottom_circles_to_remove:
                    bottom_edge.remove(circle)

            # Save data point
            all_coordinates = comm.reduce([[coord, rank] for coord in central_coordinates + right_edge + left_edge + top_edge + bottom_edge], root=0)
            if rank == 0:
                num_of_circles = len(all_coordinates)
                packing_fraction = (num_of_circles * circle_area) / box_area
                print(f"For rank {rank}, {sample_number * num_processors} samples and {num_of_circles} circles Packing fraction is {packing_fraction}")
                packing_fractions.append(packing_fraction)
                samples.append(sample_number * num_processors)

            if on_left:
                right_halo_req.wait()
            if send_veritcal_traffic and not on_bottom:
                top_halo_req.wait()

    if rank == 0:
        samples_vs_PF_DF = pd.DataFrame({"Packing Fraction": pd.Series(packing_fractions), "Number of Samples": pd.Series(samples)})
        coordinates_DF = pd.DataFrame({"x": pd.Series([coord[0][0] for coord in all_coordinates]), "y": pd.Series([coord[0][1] for coord in all_coordinates]), "rank": pd.Series([coord[1] for coord in all_coordinates])})
        plot(width, height, radius, samples_vs_PF_DF, coordinates_DF)

    return packing_fraction

main(100, 100, 1, 100000)

