def circles_are_overlapping(x1, y1, x2, y2, radius):
    """
    Checks if two circles of the same radius are overlapping
    
    :param float x1: The x coordinate of the first cirlce
    :param float y1: The y coordinate of the first cirlce
    :param float x2: The x coordinate of the second cirlce
    :param float y2: The y coordinate of the second cirlce
    :param float radius: The radius of circle 1 and 2

    :return: True if overlapping False is not.
    """
    return (((x2 - x1)**2 + (y2 - y1)**2) ** 0.5) < (2 * radius)

def get_overlapping_circles(fixed_list, changeable_list, radius):
    """
    Determins the circles in one list that overlap those of another list.
    
    :param list(list(float)) fixed_list: The first list of circles
    :param list(list(float)) changeable_list: The second list of circles
    :param float radius: The radius of every circle in both lists

    :return: A list of the elements from changeable_list which overlap at least one circle in fixed_list
    """
    circles_to_remove = []
    for circle1 in changeable_list:
        x1 = circle1[0]
        y1 = circle1[1]
        for circle2 in fixed_list:
            x2 = circle2[0]
            y2 = circle2[1]
            if circles_are_overlapping(x1, y1, x2, y2, radius):
                circles_to_remove.append(circle1)
                break
    return circles_to_remove
