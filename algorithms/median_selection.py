from ui.radar_display import RadarEntity


def oracle(dots_array: list[RadarEntity]) -> int:
    """
    Returns a good guess for the median from an array of dots. 
    It helps the main algorithm by making it possible to discard
    a big chunck of the main array.
    """

    # Base case: when the median of medians is found!
    if len(dots_array) == 1:
        return dots_array[0]

    # Grouping the elements in groups of 5
    groups_of_five = []
    for i in range(0, len(dots_array), 5):
        groups_of_five.append(dots_array[i:i+5])
    
    # Taking the median of the medians
    new_dots_array = []
    for group in groups_of_five:

        group.sort(key=lambda dot: dot.x) # Ordenates each group by coordinates X
        mid_index = len(group) // 2 
        new_dots_array.append(group[mid_index])

    return oracle(new_dots_array)
        