
import numpy as np
import pandas as pd
from mpi4py import MPI
import math

from plot_data import plot
from utils import get_overlapping_circles, new_circle_is_overlapping_existing_circles

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
    diameter = 2 * radius
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
    coordinates = []
    right_edge = []
    left_edge = []
    top_edge = []
    bottom_edge = []
    packing_fractions = [0]
    samples = [0]

    for sample_index in range(num_samples_per_processor):
        # Create a data point if this is not the first sample and either we are at the last sample or we have done a 100th of the total samples
        should_create_data_point = sample_index > 0 and (sample_index == num_samples_per_processor - 1 or (sample_index % math.floor(num_samples_per_processor * 0.01)) == 0)
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
        
        # Generate random numbers
        x_rand = np.random.random()
        y_rand = np.random.random()

        # Ensure the circle is fully in the box
        if on_left:
            x = radius + x_rand * (section_width - radius)
        else:
            x = section_x_0 + x_rand * (section_width - radius)
        
        if num_processors == 2:
            y = radius + y_rand * (section_height - diameter)
        else:
            if on_bottom:
                y = radius + y_rand * (section_height - radius)
            elif on_top:
                y = section_y_0 + y_rand * (section_height - radius)
            else:
                y = section_y_0 + y_rand * section_height
        
        circle = [x, y, sample_index]
                
        # Check if the circle is in an edge region
        if not new_circle_is_overlapping_existing_circles(x, y, coordinates, diameter):
            coordinates.append(circle)
            if x > section_x_0 + section_width - diameter:
                right_edge.append(circle)
            elif x < section_x_0 + diameter:
                left_edge.append(circle)
            
            if y > section_y_0 + section_height - diameter:
                top_edge.append(circle)
            elif y < section_y_0 + diameter:
                bottom_edge.append(circle)
            
        if should_create_data_point:
            # Remove overlapping circles in different boxes
            if on_right:
                received_left_halo = left_halo_rec.wait()
                left_circles_to_remove = get_overlapping_circles(received_left_halo, left_edge, diameter)
                left_edge = [left_edge_circle for left_edge_circle in left_edge if left_edge_circle[2] not in left_circles_to_remove]
                coordinates = [circle for circle in coordinates if circle[2] not in left_circles_to_remove]
            
            if send_veritcal_traffic and not on_bottom:
                received_bottom_halo = bottom_halo_rec.wait()
                bottom_circles_to_remove = get_overlapping_circles(received_bottom_halo, bottom_edge, diameter)
                left_edge = [bottom_edge_circle for bottom_edge_circle in bottom_edge if bottom_edge_circle[2] not in bottom_circles_to_remove]
                coordinates = [circle for circle in coordinates if circle[2] not in bottom_circles_to_remove]

            # Save data point
            all_coordinates = comm.reduce([[coord, rank] for coord in coordinates], root=0)
            if rank == 0:
                num_of_circles = len(all_coordinates)
                packing_fraction = (num_of_circles * circle_area) / box_area
                sample_number = sample_index + 1
                print(f"For rank {rank}, {sample_number * num_processors} samples and {num_of_circles} circles Packing fraction is {packing_fraction}")
                packing_fractions.append(packing_fraction)
                samples.append(sample_number * num_processors)

            if on_left:
                right_halo_req.wait()
            if send_veritcal_traffic and not on_top:
                top_halo_req.wait()

    if rank == 0:
        samples_vs_PF_DF = pd.DataFrame({"Packing Fraction": pd.Series(packing_fractions), "Number of Samples": pd.Series(samples)})
        coordinates_DF = pd.DataFrame({"x": pd.Series([coord[0][0] for coord in all_coordinates]), "y": pd.Series([coord[0][1] for coord in all_coordinates]), "rank": pd.Series([coord[1] for coord in all_coordinates])})
        plot(width, height, radius, samples_vs_PF_DF, coordinates_DF)

main(100, 100, 1, 100000)

