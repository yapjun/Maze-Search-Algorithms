import math
import time
import heapq


def get_neighbours(current, maze, visited):
    """
    Returns all valid neighbours of the current Node

    Parameters:
        current   (tuple): Contains the Node's current position
        maze   (2-d list): Contains the maze. Used to check if Node
                           is within bounds
        visited     (set): Contains a list of visited nodes. Used to
                           filter out neighbours that have already been
                           visited.

    Returns:
        neighbours (list): Contains a list of valid neighbours

    """

    r = current[0]
    c = current[1]

    # top right left bottom priority
    all_neighbours = [(r - 1, c),
                      (r, c + 1),
                      (r, c - 1),
                      (r + 1, c), ]
    neighbours = []

    # filters valid neighbours
    for each in all_neighbours:
        # go next if out of bounds, is a wall or visited
        if each in visited:
            continue
        if each[0] < 0 or each[0] > len(maze) - 1:  # row bounds check
            continue
        if each[1] < 0 or each[1] > len(maze[0]) - 1:  # column bounds check
            continue
        if maze[each[0]][each[1]] == '#':
            continue

        # append and return list of valid neighbours
        neighbours.append(each)
    return neighbours


def get_path(node):
    """
    Loops through all Nodes preceding the current_node and
    compiles it into the final path.

    Args:
        node  (Node): Node object

    Returns:
        path  (list): Contains full path from start to the end Node.
    """

    path = [node.position]

    # get final path by going through node parents
    while node.parent:
        node = node.parent
        path.append(node.position)
    return path[::-1]


# euclidean is slower with an average of 0.8 seconds on VLarge
def euclidean(current, end):
    """
    Calculates and returns the Euclidean heuristic of the given Node

    Args:
        current  (tuple): Position of the current Node
        end      (tuple): Position of the end Node

    Returns:
        Euclidean heuristic for the given Node
    """

    return math.sqrt((current[0] - end[1]) ** 2 + (current[1] - end[1]) ** 2)


# an average of 0.5 seconds on VLarge
def manhattan(current, end):
    """
    Calculates and returns the Manhattan heuristic of the given Node

    Args:
        current  (tuple): Position of the current Node
        end      (tuple): Position of the end Node

    Returns:
        Manhattan heuristic for the given Node
    """
    return abs(current[0] - end[0]) + abs(current[1] - end[1])


class Node:
    """
    To represent Node, to be used with A-Star search

    Attributes:
        parent     (Node): Node, the parent of self
        position  (tuple): Tuple, position of current node
        f           (int): Absolute value of some number, contains
                           the heuristic value of the current Node.
    """

    # default constructor with default values if unset
    def __init__(self, parent=None, position=None, f=0):
        self.parent = parent
        self.position = position
        self.f = f

    # comparison methods for heap purposes
    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.f)


def astar(maze, start, end):
    """
    Solves the maze given using A-Star Search, returns statistics and pathing.

    Args:
            maze  (2-d list): Contains the maze
            start    (tuple): Position of the starting position
            end      (tuple): Position of the end position

    Returns:
            path      (list): Contains all the tiles traversed from the
                              start node in order to reach the end node.
            closed     (set): Contains all Nodes explored while trying
                              to find the path.
    """

    # initialize open, closed, step count, and start_time
    open = []
    closed = set()
    steps = 0
    start_time = time.time()

    # create start_node with no parent and push into heap
    start_node = Node(None, start, manhattan(start, end))
    heapq.heappush(open, (start_node.f, start_node))

    # loop while the heap open contains elements
    while open:
        # retrieve node with the smallest f value from heap and add it to closed
        current = heapq.heappop(open)
        closed.add(current[1].position)

        # check for end goal, print statistics and return if True
        if current[1].position == end:
            print("\nA-Star Search:\nNodes explored: %i\nTime taken: %s\nPath length: %i steps"
                  % (len(closed),
                     time.time() - start_time,
                     len(get_path(current[1]))))
            return get_path(current[1]), closed

        # get neighbours and update path length
        neighbours = get_neighbours(current[1].position, maze, closed)
        steps += 1

        # calculate heuristic, push with node into the heap
        for each in neighbours:
            f = manhattan(each, end) + steps
            heapq.heappush(open, (f, Node(parent=current[1], position=each, f=f)))
