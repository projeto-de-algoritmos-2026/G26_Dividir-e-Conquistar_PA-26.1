import math
from ui.radar_display import RadarEntity
from algorithms.median_selection import exotericSelect

def distance(p1: RadarEntity, p2: RadarEntity) -> float:
    """Calcula a distância euclidiana entre dois pontos"""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def brute_force_closest_pair(points: list[RadarEntity]):
    """
    Abordagem de força bruta para encontrar o par de pontos mais próximo
    Usado como caso base
    """
    min_dist = float('inf')
    closest_pair = None
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
                
    return min_dist, closest_pair

def closest_pair_recursive(px: list[RadarEntity], py: list[RadarEntity]):
    """
    Função recursiva principal de Dividir e Conquistar utilizando MOM
    """
    n = len(px)
    
    if n <= 3:
        return brute_force_closest_pair(px)

    mid_index = n // 2
    mid_point = exotericSelect(px, mid_index)

    px_left = []
    px_right = []
    left_count = 0
    
    for p in px:
        if p.x < mid_point.x:
            px_left.append(p)
            left_count += 1
        elif p.x > mid_point.x:
            px_right.append(p)

    for p in px:
        if p.x == mid_point.x:
            if left_count < mid_index:
                px_left.append(p)
                left_count += 1
            else:
                px_right.append(p)

    left_set = set(px_left)
    py_left = []
    py_right = []
    
    for p in py:
        if p in left_set:
            py_left.append(p)
        else:
            py_right.append(p)

    dl, pair_l = closest_pair_recursive(px_left, py_left)
    dr, pair_r = closest_pair_recursive(px_right, py_right)

    if dl < dr:
        d = dl
        min_pair = pair_l
    else:
        d = dr
        min_pair = pair_r

    strip = []
    for p in py:
        if abs(p.x - mid_point.x) < d:
            strip.append(p)

    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):
            dist = distance(strip[i], strip[j])
            if dist < d:
                d = dist
                min_pair = (strip[i], strip[j])

    return d, min_pair

def get_closest_pair(points: list[RadarEntity]):
    """
    Função de entrada para o algoritmo Closest Pair of Points
    """
    if not points or len(points) < 2:
        return float('inf'), None

    px = points[:] 
    py = sorted(points, key=lambda p: p.y)

    return closest_pair_recursive(px, py)
