import random
import csv

import tools
from ways import load_map_from_csv

roads = load_map_from_csv()


def is_in_list(id_, lst):
    for child in lst:
        if child[1] == id_:
            return True, child
    return False, None


###
# function to create with all necessary values.
###
def Node(current, distance, parent):
    return [distance, current,
            roads[current].links, parent]


def f(node, lat, lon):
    return tools.compute_distance(lat1=lat, lon1=lon, lat2=roads[node].lat, lon2=roads[node].lon)


def get_last_node(node, depth):
    if depth == 0 or len(node.links) == 0:
        return node
    link_indx = random.randint(0, len(node.links) - 1)
    index = node.links[link_indx].target
    return get_last_node(roads[index], depth - 1)


def initialize_search_problems(roads):
    problems_lst = []
    for sample in random.sample(range(len(roads.junctions())), 100):
        start_node = roads[sample]
        depth = random.randint(1, random.randint(1, 100))
        end_node = get_last_node(start_node, depth)
        problems_lst.append([start_node.index, end_node.index])
    with open('problems.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for problem in problems_lst:
            writer.writerow(problem)


def get_path(closed_list, source, target):
    parent = closed_list[target]
    route = [target]
    while parent is not None:
        route.append(parent)
        parent = closed_list[parent]
    route.reverse()
    return route
