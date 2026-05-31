from ui.radar_display import RadarEntity


def oracle(dots_array: list[RadarEntity]) -> int:
    """
    Returns a good guess for the median from an array of dots. 
    It helps the main algorithm by making it possible to discard
    a big chunck of dots from the main array.
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


def exotericSelect(dots_array: list[RadarEntity], k) -> RadarEntity:
    """
    Returns the k-smallest element of an unordered array. 
    In this problem, we're going use it to return the median.
    """

    # Base case: if there's only 1 element, it's the answer
    if len(dots_array) == 1:
        return dots_array[0]

    median_guess: RadarEntity = oracle(dots_array)
    
    left: list[RadarEntity] = []
    right: list[RadarEntity] = []

    # Added because there can be dots that overlaps each other in X
    equals: list[RadarEntity] = [] 

    for dot in dots_array:
        if dot.x < median_guess.x:
            left.append(dot)
        elif dot.x > median_guess.x:
            right.append(dot)
        else:
            equals.append(dot)
    
    if k < len(left):
        return exotericSelect(left, k)
        
    elif k < len(left) + len(equals):
        return equals[0] 
        
    else:
        new_k = k - len(left) - len(equals)
        return exotericSelect(right, new_k)
    