import math
import numpy as np
from src.checkObst import is_line_circle_intersecting

def translate_pts(collision_points, center, radius):
    translated_pts = {}
    cx, cy = center[0], center[1]
    K = 0.8
    for point in collision_points:
        px, py = point[0], point[1]
        r0 = np.sqrt((px - cx) ** 2 + (py - cy) ** 2)
        rp = 2 * radius - r0  # Shift distance
        if px > cx and py > cy:
            newP_x = px + rp * math.cos(0.7853)  # shift 45 degree - 1st quadrant
            newP_y = py + rp * math.sin(0.7853)
        if px < cx and py > cy:
            newP_x = px - rp * math.cos(0.7853)  # shift 45 degree - 2nd quadrant
            newP_y = py + rp * math.sin(0.7853)
        if px < cx and py < cy:
            newP_x = px - rp * math.cos(0.7853)  # shift 45 degree - 2nd quadrant
            newP_y = py - rp * math.sin(0.7853)
        if px > cx and py < cy:
            newP_x = px + rp * math.cos(0.7853)  # shift 45 degree - 2nd quadrant
            newP_y = py - rp * math.sin(0.7853)
        if px == cx and py > cy:
            newP_x = px
            newP_y = py + rp
        if px == cx and py < cy:
            newP_x = px
            newP_y = py - rp
        if px < cx and py == cy:
            newP_x = px - rp
            newP_y = py
        if px > cx and py == cy:
            newP_x = px + rp
            newP_y = py
        translated_pts[point] = (round(newP_x, 1), round(newP_y, 1))
    return translated_pts


def adjust_roadmap(graph, collision_points, sample_nodes, obstacle_info):
    radius, center  = obstacle_info
    translated_pts = translate_pts(collision_points, center, radius)
    print('shifted points',len(collision_points), len(translated_pts), len(graph.keys()), len(sample_nodes))
    for i, point in enumerate(collision_points):
        for key, values in list(graph.items()):
            if point == key:
                valid_points = get_non_intersecting_edges(translated_pts[point], graph[point], radius, center)
                graph[translated_pts[point]] = list(valid_points)
                del graph[point]
            if point in set(values):
                index = values.index(point)
                if is_line_circle_intersecting(key, translated_pts[point], center, radius):
                    del values[index]
                else:
                    values[index] = translated_pts[point]
    sample_nodes.update(translated_pts.values())
    print('adjusted',len(sample_nodes), len(graph.keys()))
    return graph


def get_non_intersecting_edges(point1, child_points, radius, center):
    valid_points = []
    for child in child_points:
        if not is_line_circle_intersecting(point1, child, center, radius):
            valid_points.append(child)
    return set(valid_points)

