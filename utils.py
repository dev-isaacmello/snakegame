import math

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def find_closest_food(position, food_list):
    if not food_list:
        return None

    closest = food_list[0]
    min_dist = distance_vec(position, closest.position)

    for food in food_list[1:]:
        dist = distance_vec(position, food.position)
        if dist < min_dist:
            min_dist = dist
            closest = food

    return closest

def distance_vec(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])