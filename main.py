'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions


from utils import *


def huristic_function(lat1, lon1, lat2, lon2):
    ###
    # The function will compute direct distance and devide it by the max speed of all roads == (110).
    ###
    res = implement_heuristic_function(lat1, lon1, lat2, lon2)
    return res[0]


def find_ucs_rout(source, target):
    'call function to find path, and return list of indices'
    res = implement_ucs(source, target)
    return res[0]


def find_astar_route(source, target):
    res = implement_astar(source, target)
    return res[0]


def find_idastar_route(source, target):
    'call function to find path, and return list of indices'
    res = implement_idastar(source, target)
    return res


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
    # algorithm_on_problems(filename="problems.csv", algo='find_ucs_rout', write_to="results/UCSRuns.txt")
    # algorithm_on_problems(filename="problems.csv", algo='find_astar_route', write_to="results/AStarRuns.txt")
    create_map()
    # algorithms_time_measure()
