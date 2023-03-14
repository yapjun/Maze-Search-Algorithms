# -*- coding: utf-8 -*-
import time
import heapq
import math

FROM_START = 1
FROM_END = 2


class BiStruct:
    """
    To keep a collection of nodes and maze data, to assist
    with the search algorithm

    Attributes:
        start_time     (time): Marks the start of the function runtime.
        fwd_open       (heap): Open list for the search for direction FROM_START.
        bwd_open       (heap): Open list for the search for direction FROM_END.
        fwd_parents    (dict): Stores parents of nodes for direction FROM_START.
        bwd_parents    (dict): Stores parents of nodes for direction FROM_END.
        fwd_visited     (set): Stores the visited nodes for direction FROM_START.
        bwd_visited     (set): Stores the visited nodes for direction FROM_END.
        start         (Tuple): The starting position of the maze (row, column).
        end           (Tuple): The end (goal) position of the maze (row, column).
    """

    # default constructor with default values if unset
    def __init__(self, start_time=time.time(), start=(0, 0), end=(0, 0), fwd_target=(0, 0), bwd_target=(0, 0),
                 fwd_current=(0, 0), bwd_current=(0, 0)):
        self.start_time = start_time

        self.fwd_open = []
        self.bwd_open = []

        # takes care of path
        self.fwd_steps = 0
        self.bwd_steps = 0

        self.fwd_parents = {}
        self.bwd_parents = {}

        self.fwd_visited = set()
        self.bwd_visited = set()

        self.fwd_current = fwd_current
        self.bwd_current = bwd_current
        self.fwd_target = fwd_target
        self.bwd_target = bwd_target

        self.start = start
        self.end = end


def bi_a_star(maze, start, end):
    """
    Solves the given maze by applying the bidirectional A* search algorithm

    Args:
        maze   (2-d list): Contains the maze
        start     (tuple): Position of the starting position
        end       (tuple): Position of the end position

    Returns:
        path       (list): Contains all the tiles traversed from the
                           start node in order to reach the end node.
        closed      (set): Contains all Nodes explored while trying
                           to find the path.
    """

    # initialize BiStruct, add start and end to visited, push into open list, set parents
    bi = BiStruct(start=start, end=end, fwd_target=end, bwd_target=start, fwd_current=start, bwd_current=end)

    # search forwards
    bi.fwd_visited.add(start)
    heapq.heappush(bi.fwd_open, (heuristic(start, end, start, FROM_START), start))
    bi.fwd_parents[start] = None

    # search backwards
    bi.bwd_visited.add(end)
    heapq.heappush(bi.bwd_open, (heuristic(end, start, end, FROM_END), end))
    bi.bwd_parents[end] = None

    while bi.fwd_open and bi.bwd_open:
        # check for intersections, return path if found

        # explore FROM_START to end
        intersection = explore_neighbours(bi, FROM_START, maze)
        if intersection:
            return bi_get_path(bi, intersection)

        # explore FROM_END to start
        intersection = explore_neighbours(bi, FROM_END, maze)
        if intersection:
            return bi_get_path(bi, intersection)

    return "Path not found!"


def heuristic(start, target, current, direction):
    """
    Calculates heuristics depending on the direction
    The so-called "average function" by Goldberg.

    Args:
        start     (tuple): The starting position of the maze (row, column).
        target    (tuple): Target position
        current   (tuple): Contains the current Node's position
        direction   (int): To distinguish between the 2 directions (FROM_START, FROM_END)
    """

    fwd = math.sqrt((current[0] - target[1]) ** 2 + (current[1] - target[1]) ** 2)
    bwd = math.sqrt((start[0] - current[0]) ** 2 + (start[1] - current[1]) ** 2)
    heur_value = (fwd - bwd) / 2.0

    if direction == FROM_START:
        return abs(heur_value)
    else:
        return -abs(heur_value)


def explore_neighbours(struct: BiStruct, direction, maze):
    """ 
    Explore all valid neighbours, store in open lists, visited, and append parents

    Args:
        struct    (BiStruct): A collection of Node and maze data
        direction      (int): To distinguish between the 2 directions (FROM_START, FROM_END)
        maze      (2-d list): Contains the maze, used to check if position is valid

    Returns:
        nodes        (tuple): If found, the intersection node.
    """

    if direction == FROM_START:
        current = heapq.heappop(struct.fwd_open)
        struct.fwd_target = struct.bwd_current
        nodes = get_neighbours(current[1], struct, maze, struct.fwd_visited)

        # if a tuple is returned, an intersection is found
        if isinstance(nodes, tuple):
            return nodes

        struct.fwd_steps += 1
        for each in nodes:
            # g = manhattan(current[1], struct.fwd_target, FROM_START)
            g = heuristic(struct.bwd_target, struct.fwd_target, current[1], FROM_START)
            f = g + struct.fwd_steps

            heapq.heappush(struct.fwd_open, (f, each))
            struct.fwd_visited.add(each)
            struct.fwd_parents[each] = current[1]

        # set current node so that FROM_END works towards the intersection
        struct.fwd_current = current[1]

    else:
        current = heapq.heappop(struct.bwd_open)
        struct.bwd_target = struct.fwd_current
        nodes = get_neighbours(current[1], struct, maze, struct.bwd_visited)
        struct.bwd_steps += 1

        # if a tuple is returned, an intersection is found
        if isinstance(nodes, tuple):
            return nodes

        for each in nodes:
            g = heuristic(struct.bwd_target, struct.fwd_target, current[1], FROM_END)
            # g = manhattan(current[1], struct.bwd_target, FROM_START)
            f = g + struct.bwd_steps

            heapq.heappush(struct.bwd_open, (f, each))
            struct.bwd_visited.add(each)
            struct.bwd_parents[each] = current[1]

        struct.bwd_current = current[1]


def get_neighbours(current, struct: BiStruct, maze, visited):
    """
    Check and return intersection if found, else filter and return
     all valid neighbours of the current Node

    Args:
        current        (tuple): Contains the current Node's position
        struct      (BiStruct): A collection of node and maze data
        maze        (2-d list): Contains the maze
        visited          (set): Current direction's visited nodes.
    Returns:
        each           (tuple): If found, the intersection node
        neighbours      (list): Contains a list of valid neighbours

    """

    r = current[0]
    c = current[1]

    # top right left bottom priority, but doesn't matter for A*
    all_neighbours = [(r - 1, c),
                      (r, c + 1),
                      (r, c - 1),
                      (r + 1, c), ]
    neighbours = []

    # filters valid neighbours
    for each in all_neighbours:
        # if node has been visited by both directions, return intersection
        if each in struct.fwd_visited and each in struct.bwd_visited:
            return each
        if each in visited:
            continue
        if each[0] < 0 or each[0] > len(maze) - 1:  # row bounds check
            continue
        if each[1] < 0 or each[1] > len(maze[0]) - 1:  # column bounds check
            continue
        if maze[each[0]][each[1]] == '#':
            continue
        # no intersection, return list of valid neighbours
        neighbours.append(each)
    return neighbours


# an average of 0.5 seconds on VLarge
def manhattan(current, end, direction):
    """
    Calculates and returns the Manhattan heuristic of the given Node

    Args:
        current  (tuple): Position of the current Node
        end      (tuple): Position of the end Node

    Returns:
        Manhattan heuristic for the given Node
    """
    value = abs(current[0] - end[0]) + abs(current[1] - end[1])
    if direction == FROM_START:
        return value
    else:
        return -abs(value)


def bi_get_path(struct: BiStruct, intersect_node):
    """
    Compiles paths and visited from both directions

    Args:
        struct        (BiStruct): A collection of node and maze data
        intersect_node   (tuple): Intersection node,
                                  Acts as middle point to combine the 2 paths

    Returns:
        path              (list): Full path from start to end
        all_visited        (set): All visited paths from the algorithm
    """

    path = list()
    path.append(intersect_node)
    i = intersect_node

    while i != struct.start:
        path.append(struct.fwd_parents[i])
        i = struct.fwd_parents[i]

    path = path[::-1]

    i = intersect_node

    while i != struct.end:
        path.append(struct.bwd_parents[i])
        i = struct.bwd_parents[i]

    all_visited = struct.fwd_visited.union(struct.bwd_visited)
    print("\nBidirectional A* Search:\nNodes explored: %i\nTime taken: %s\nPath length: %i steps"
          % (len(all_visited),
             time.time() - struct.start_time,
             len(path)))
    return path, all_visited
