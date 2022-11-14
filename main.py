'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
from collections import deque

import heapq

import info
import tools
from ways import load_map_from_csv

from utils import *


roads = load_map_from_csv()

def huristic_function(lat1, lon1, lat2, lon2):
    ###
    # The function will compute direct distance and devide it by the max speed of all roads == (110).
    ###
    max_speed = 110
    dist = tools.compute_distance(lat1, lon1, lat2, lon2)
    return dist / max_speed


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    node = [0.0, source, roads[source].links, None]
    lat = roads[source].lat
    lon = roads[source].lon
    frontier = []
    closed_list = {}
    heapq.heappush(frontier, node)
    while frontier:
        ###
        # Node => [dist_from_source, current_id, links, parent_id]
        #         [       0        ,      1    ,   2  ,      3    ]
        ###
        node = heapq.heappop(frontier)
        if node[1] == target:
            res = get_path(closed_list, source, target)
            return res
        # set current Node id to its parent (node[3] -> is the parent of node).
        parent_id = node[1]
        # expand node
        if parent_id not in closed_list:
            closed_list[parent_id] = None
        for link in node[2]:
            # initialize child's node.
            child = [node[0] + link.distance, link.target, roads[link.target].links, node[1]]
            current_id = child[1]
            in_frontier, temp_child = is_in_list(child[1], frontier)
            if child[1] not in closed_list.keys() and (not in_frontier):
                frontier.append(child)
                closed_list[current_id] = parent_id
            elif in_frontier and child[0] < temp_child[0]:
                frontier.remove(temp_child)
                heapq.heappush(frontier, child)
                # update parent id.
                closed_list[current_id] = parent_id
    return None, []


def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    # Initialize first node.
    node = [huristic_function(lat1=roads[source].lat, lon1=roads[source].lon, lat2=roads[target].lat,
                              lon2=roads[target].lon), source, roads[source].links, None, 0]
    src_lat = roads[source].lat
    src_lon = roads[source].lon
    frontier = []
    closed_list = {}
    heapq.heappush(frontier, node)
    while frontier:
        ###
        # Node => [f() + h(), current_id, links, parent_id, distance_from_source]
        #         [   0     ,      1    ,   2  ,      3   ,         4           ]
        ###
        node = heapq.heappop(frontier)
        if node[1] == target:
            res = get_path(closed_list, source, target)
            return res
        # set current Node id to its parent (node[3] -> is the parent of node).
        parent_id = node[1]
        # expand node
        if parent_id not in closed_list:
            closed_list[parent_id] = None
        for link in node[2]:
            # initialize child node.
            ###
            # The next two lines, calculate the new f() and h().
            ###
            h_price = huristic_function(src_lat, src_lon, roads[link.target].lat, roads[link.target].lon)
            f_price = (node[4] + link.distance) / info.SPEED_RANGES[link.highway_type][1]
            # Create next child's Node.
            child = [f_price + h_price, link.target, node[2], node[1], f_price]
            current_id = child[1]
            in_frontier, temp_child = is_in_list(child[1], frontier)
            if child[1] not in closed_list.keys() and (not in_frontier):
                frontier.append(child)
                closed_list[current_id] = parent_id
            elif in_frontier and child[0] < temp_child[0]:
                frontier.remove(temp_child)
                heapq.heappush(frontier, child)
                # update parent id.
                closed_list[current_id] = parent_id
    return None, []


def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv

    # dispatch(argv)
    ucs_on_problems("problems.csv")
