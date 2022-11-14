import random
import csv

import tools
from main import find_ucs_rout
from ways import load_map_from_csv

from main import roads

from main import *

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


def ucs_on_problems(filename):
    import csv
    problems_list = []
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            problems_list.append([row[0], row[1]])
    f = open("results/UCSRuns.txt", "w")
    for problem in problems_list:
        f.write(find_ucs_rout(int(problem[0]), int(problem[1])))
    f.close()


def get_path(closed_list, source, target):
    parent = closed_list[target]
    route = [target]
    while parent is not None:
        route.append(parent)
        parent = closed_list[parent]
    route.reverse()
    return route
