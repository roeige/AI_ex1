'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

import random
import csv

from ways import load_map_from_csv


def initialize_search_problems(roads):
    problems_lst = []
    for sample in random.sample(range(len(roads.junctions())), 100):
        start_node = roads[sample]
        depth = random.randint(0, len(start_node.links))
        end_node = get_last_node(start_node, depth, roads)
        problems_lst.append([start_node.index, end_node.index])
    with open('problems.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for problem in problems_lst:
            writer.writerow(problem)


def get_last_node(node, depth, roads):
    if depth == 0 or len(node.links) == 0:
        return node
    link_indx = random.randint(0, len(node.links) - 1)
    index = node.links[link_indx].target
    return get_last_node(roads[index], depth - 1, roads)


def huristic_function(lat1, lon1, lat2, lon2):
    raise NotImplementedError


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError


def find_astar_route(source, target):
    'call function to find path, and return list of indices'
    raise NotImplementedError


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
    roads = load_map_from_csv()
    initialize_search_problems(roads)
