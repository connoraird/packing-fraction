def circles_are_overlapping(x1, y1, x2, y2, radius):
    return (((x2 - x1)**2 + (y2 - y1)**2) ** 0.5) < (2 * radius)

def get_overlapping_circles(fixed_list, changeable_list, radius):
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
