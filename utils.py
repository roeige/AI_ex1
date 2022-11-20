#Roei Gehassi, 208853754
import heapq
import random
import csv
import sys

from matplotlib import pyplot as plt
import time
import draw
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
    node = [0, source, roads[source].links, None]
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
            path = get_path(closed_list, source, target)
            total_time = node[0]
            return path, total_time
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
            g_price = node[0] + g(link.distance, speed_limit)
            child = [g_price, link.target, roads[link.target].links, node[1]]
            current_id = child[1]
            in_frontier, temp_child = is_in_list(child[1], frontier)
            if child[1] not in closed_list.keys() and (not in_frontier):
                heapq.heappush(frontier, child)
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


def g(metric_dist, speed_limit):
    return (metric_dist / 1000) / speed_limit


def implement_heuristic_function(lat1, lon1, lat2, lon2):
    max_speed = 110
    dist = tools.compute_distance(lat1, lon1, lat2, lon2)
    return dist / max_speed


def implement_astar(source, target):
    'call function to find path, and return list of indices'
    # Initialize first node.
    h_start = implement_heuristic_function(lat1=roads[source].lat, lon1=roads[source].lon, lat2=roads[target].lat,
                                           lon2=roads[target].lon)
    node = [h_start, source, roads[source].links, None, 0]
    h_lat = roads[target].lat
    h_lon = roads[target].lon
    frontier = []
    closed_list = {}
    heapq.heappush(frontier, node)
    while frontier:
        ###
        # Node => [g() + h(), current_id, links, parent_id,      g() from source  ]
        #         [   0     ,      1    ,   2  ,      3   ,           4           ]
        ###
        node = heapq.heappop(frontier)
        if node[1] == target:
            path = get_path(closed_list, source, target)
            total_time = node[4]
            return path, total_time, h_start
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
            h_price = implement_heuristic_function(roads[link.target].lat, roads[link.target].lon, h_lat, h_lon)
            g_price = node[4] + g(link.distance, info.SPEED_RANGES[link.highway_type][1])
            # Create next child's Node.
            child = [g_price + h_price, link.target, roads[link.target].links, node[1], g_price]
            current_id = child[1]
            in_frontier, temp_child = is_in_list(child[1], frontier)
            if child[1] not in closed_list.keys() and (not in_frontier):
                heapq.heappush(frontier, child)
                closed_list[current_id] = parent_id
            elif in_frontier and child[0] < temp_child[0]:
                frontier.remove(temp_child)
                heapq.heappush(frontier, child)
                # update parent id.
                closed_list[current_id] = parent_id
    return None, [], 0


def initialize_search_problems():
    problems_lst = []
    for sample in random.sample(range(len(roads.junctions())), 100):
        start_node = roads[sample]
        depth = random.randint(1, random.randint(4, 100))
        end_node = get_last_node(start_node, depth)
        problems_lst.append([start_node.index, end_node.index])
    with open('problems.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for problem in problems_lst:
            writer.writerow(problem)


def algorithm_on_problems(filename, algo, write_to):
    import csv
    problems_list = []
    x = []
    y = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            problems_list.append([row[0], row[1]])
    f = open(write_to, "w")
    for problem in problems_list:
        if algo == 'find_astar_route':
            path, total_time, h_time = algo_dict[algo](int(problem[0]), int(problem[1]))
            total_time = f'{total_time:.5f}'[:-1]
            h_time = f'{h_time:.5f}'[:-1]
            x.append(h_time)
            y.append(total_time)

            f.write(str(' '.join(str(j) for j in path)) + ' - ' + str(total_time) + ' - ' + str(h_time) + '\n')
        else:
            path, total_time = algo_dict[algo](int(problem[0]), int(problem[1]))
            total_time = f'{total_time:.5f}'[:-1]
            path = ' '.join(str(j) for j in path)
            f.write(str(path) + ' - ' + str(total_time) + '\n')
    f.close()
    if algo == 'find_astar_route':
        get_graph(x, y)


new_limit = 0


def implement_idastar(source, target):
    h_start = implement_heuristic_function(lat1=roads[source].lat, lon1=roads[source].lon, lat2=roads[target].lat,
                                           lon2=roads[target].lon)
    node = [h_start, source, roads[source].links, None, 0]
    h_lat = roads[target].lat
    h_lon = roads[target].lon
    global new_limit
    new_limit = h_start
    while True:
        f_limit = new_limit
        new_limit = sys.maxsize
        solution = DFS_f(node, g_val=0, path=[source], f_limit=f_limit, target=target, h_lat=h_lat, h_lon=h_lon)
        if solution:
            return solution


def DFS_f(node, g_val, path, f_limit, target, h_lat, h_lon):
    global new_limit
    new_f = g_val + implement_heuristic_function(roads[node[1]].lat, roads[node[1]].lon, h_lat, h_lon)
    if new_f > f_limit:
        new_limit = min(new_limit, new_f)
        return []
    if node[1] == target:
        return path
    for link in node[2]:
        h_price = implement_heuristic_function(roads[link.target].lat, roads[link.target].lon, h_lat, h_lon)
        g_price = node[4] + g(link.distance, info.SPEED_RANGES[link.highway_type][1])
        # Create next child's Node.
        child = [g_price + h_price, link.target, roads[link.target].links, node[1], g_price]
        solution = DFS_f(child, g_val + (h_price + g_price), path + [child[1]], f_limit, target, h_lat, h_lon)
        if solution:
            return solution
    return []


def create_map():
    problems = [[944770, 944768], [83737, 83736], [36053, 36056], [275843, 308448], [175055, 175053], [280930, 280929],
                [503690, 497555], [190525, 190522], [312559, 253967], [71225, 71211]]
    for problem in problems:
        path = implement_idastar(int(problem[0]), int(problem[1]))
        draw.plot_path(roads, path, 'g')
        plt.savefig("solutions_img/" + str(problem[0]) + '-' + str(problem[1]))
        plt.close()


def get_path(closed_list, source, target):
    if source == target:
        return [source]
    parent = closed_list[target]
    route = [target]
    while parent is not None:
        route.append(parent)
        parent = closed_list[parent]
    route.reverse()
    return route


###
# function to create graph from X - > array of x-axis' points and Y -> y-axis' points
###
def get_graph(x, y):
    plt.plot(x, y, 'o')
    plt.xlabel('Heuristic drive time')
    plt.ylabel('Actual drive time')
    plt.title('Heuristic vs Actual time graph')
    plt.show()
    plt.close()


def algorithms_time_measure():
    problems = [[944770, 944768], [83737, 83736], [36053, 36056], [275843, 308448], [175055, 175053], [280930, 280929],
                [503690, 497555], [190525, 190522], [312559, 253967], [71225, 71211]]
    start = time.time()
    end = time.time()
    ucs_time = run_algo(problems, 'find_ucs_rout')
    astar_time = run_algo(problems, 'find_astar_route')
    idastar_time = run_algo(problems, 'find_idastar')
    print('ucs time : ' + str(ucs_time) + '\n' + 'astar time : ' + str(astar_time) + '\n' + 'idastar time : '
          + str(idastar_time) + '\n')


def run_algo(problems, algo):
    start = time.time()
    for problem in problems:
        algo_dict[algo](problem[0], problem[1])
    end = time.time()
    res = (end - start) / 10
    return f'{res:.6f}'[:-1]


# algorithms dictionary.
algo_dict = {'find_ucs_rout': implement_ucs, 'find_astar_route': implement_astar, 'find_idastar': implement_idastar}
