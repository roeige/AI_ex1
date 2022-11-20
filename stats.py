'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

#Roei Gehassi, 208853754
import sys
from collections import namedtuple
from ways import load_map_from_csv
from collections import Counter


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    res = {}
    total_links = 0
    max_branching_factor = 0
    min_branching_factor = sys.maxsize
    branching_sum = 0
    max_link_distance = 0
    min_link_distance = sys.maxsize
    sum_link_distance = 0
    links_type_list = []
    for junction in roads.junctions():
        total_links += len(junction.links)
        max_branching_factor = max(max_branching_factor, len(junction.links))
        min_branching_factor = min(min_branching_factor, len(junction.links))
        max_temp = 0
        min_temp = sys.maxsize
        for link in junction.links:
            max_temp = max(link.distance, max_temp)
            min_temp = min(link.distance, min_temp)
            links_type_list.append(link.highway_type)
            sum_link_distance += link.distance
        max_link_distance = max(max_link_distance, max_temp)
        min_link_distance = min(min_link_distance, min_temp)
        branching_sum += len(junction.links)
    res["Number of junctions"] = len(roads.junctions())
    res["Number of links"] = total_links
    res["Outgoing branching factor"] = Stat(max_branching_factor, min_branching_factor,
                                            branching_sum / len(roads.junctions()))
    res["Link distance"] = Stat(max_link_distance, min_link_distance, sum_link_distance / total_links)
    res["Link type histogram"] = dict(Counter(links_type_list))
    return res


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))


if __name__ == '__main__':
    from sys import argv

    assert len(argv) == 1
    print_stats()
