def get_overlapping_circles(fixed_list, changeable_list, diameter):
    """
    Determines the circles in one list that overlap those of another list.
    
    :param list(list(float)) fixed_list: The first list of circles
    :param list(list(float)) changeable_list: The second list of circles
    :param float radius: The radius of every circle in both lists

    :return: A list of the elements from changeable_list which overlap at least one circle in fixed_list
    """
    circles_to_remove = []
    for circle1 in changeable_list:
        x1 = circle1[0]
        y1 = circle1[1]
        if new_circle_is_overlapping_existing_circles(x1, y1, fixed_list, diameter):
            circles_to_remove.append(circle1[2])
    return circles_to_remove

def new_circle_is_overlapping_existing_circles(new_x, new_y, existing_circles, diameter):
    """
    Checks if a new set of circle coordinates overlaps with any existing circles in a given list

    :param float new_x: The x coordinate of the new circle
    :param float new_y: The y coordinate of the new circle
    :param list(list(float)) existing_circles: A list of existing circle coordinates
    :param floar radius: The radius of every circle

    :return: True is new cirlce overlaps an existing one, otherwise returns False
    """
    overlapping = False
    for circle in existing_circles:
        x_to_check = circle[0]
        y_to_check = circle[1]
        if (((x_to_check - new_x)**2 + (y_to_check - new_y)**2) ** 0.5) < diameter:
            overlapping = True
            break
    return overlapping
