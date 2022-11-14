import heapq
import random
import csv

import info
import tools
from main import find_ucs_rout
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
def Node(distance, current, parent):
    return [distance, current,
            roads[current].links, parent]


def get_last_node(node, depth):
    if depth == 0 or len(node.links) == 0:
        return node
    link_indx = random.randint(0, len(node.links) - 1)
    index = node.links[link_indx].target
    return get_last_node(roads[index], depth - 1)


def implement_ucs(source, target):
    node = [0.0, source, roads[source].links, None]
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
            res, total_time = get_path(closed_list, source, target, node[0])
            return res, total_time
        # set current Node id to its parent (node[3] -> is the parent of node).
        parent_id = node[1]
        # expand node
        if parent_id not in closed_list:
            closed_list[parent_id] = None
        for link in node[2]:
            ###
            # initialize child's node.
            ###
            # Next two lines calculate current link's time.
            speed_limit = info.SPEED_RANGES[link.highway_type][1]
            link_time = link.distance / speed_limit
            child = [f(node[0], link_time), link.target, roads[link.target].links, node[1]]
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


###
# function to calculate f() function from source till current node.
###
def f(old_time, curr_time):
    return old_time + curr_time


def implement_huristic_function(lat1, lon1, lat2, lon2):
    max_speed = 110
    dist = tools.compute_distance(lat1, lon1, lat2, lon2)
    return dist / max_speed


def implement_astar(source, target):
    'call function to find path, and return list of indices'
    # Initialize first node.
    node = [implement_huristic_function(lat1=roads[source].lat, lon1=roads[source].lon, lat2=roads[target].lat,
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
            res, total_time = get_path(closed_list, source, target, total_time=node[0])
            return res, total_time
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
            h_price = implement_huristic_function(src_lat, src_lon, roads[link.target].lat, roads[link.target].lon)
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


def initialize_search_problems():
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


def algorithm_on_problems(filename, algo, write_to):
    import csv
    problems_list = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            problems_list.append([row[0], row[1]])
    f = open(write_to, "w")
    for problem in problems_list:
        path, total_time = algo_dict[algo](int(problem[0]), int(problem[1]))
        f.write(str(path) + ' - ' + str(total_time) + '\n')
    f.close()


def get_path(closed_list, source, target, total_time):
    if source == target:
        return [source], 0
    parent = closed_list[target]
    route = [target]
    while parent is not None:
        route.append(parent)
        parent = closed_list[parent]
    route.reverse()
    return route, total_time


# algorithms dictionary.
algo_dict = {'find_ucs_rout': implement_ucs, 'find_astar_route': implement_astar}
