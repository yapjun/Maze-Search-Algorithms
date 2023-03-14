import time


def get_neighbours(current, maze, visited):
    """
    Returns all valid neighbours of the current Node

    Args:
        current      (tuple): Tuple containing the Node's current position.
        maze          (list): Contains the maze.
                              Used to check if Node is within bounds
        visited        (set): Contains a list of visited nodes. Used to filter out neighbours
                              that have already been visited.

    Returns:
        neighbours    (list): Contains a list of valid neighbours

    """

    r = current[0]
    c = current[1]

    # top left right bottom priority but
    # stack: last in first out
    # so technically bottom right left top
    all_neighbours = [(r - 1, c),
                      (r, c - 1),
                      (r, c + 1),
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


def dfs(maze, start, end):
    """
    Solves the maze given using Depth-First Search,
        returns statistics and pathing.

    Args:
        maze      (list): Array containing the maze, should be the return
                            value of read_maze(filename)
        start    (tuple): (r,c) of the starting position
        end      (tuple): (r,c) of the end position

    Returns:
        path      (list): Contains all the tiles traversed from the
                          start node in order to reach the end node
        visited    (set): All Nodes explored while trying to find the path
    """

    # initialize path, stack, visited and start_time
    path = []
    stack = []
    visited = set()
    start_time = time.time()
    stack.append((start, [start]))

    while stack:
        # pop the top from stack
        (current, path) = stack.pop()
        if current == end:
            print("\nDepth-First Search:\nNodes explored: %i\nTime taken: %s\nPath length: %i steps"
                  % (len(visited),
                     time.time() - start_time,
                     len(path)))
            return path, visited

        neighbours = get_neighbours(current, maze, visited)
        visited.add(current)

        for neighbour in neighbours:
            stack.append((neighbour, path + [neighbour]))

    return path
