import pygame
import sys


def read_maze(file_name):
    """
    Read the maze from a .txt file and returns maze in
    an array.

    Args:
        file_name  (str): The .txt file of the maze to be read

    Returns:
        maze      (list): Contains the maze
    """

    # initialize maze
    maze = []

    # open file and read the entire file
    file = open(file_name, "r")
    rows = file.readlines()
    for r in rows:
        # strip and check for empty lines
        row = r.strip()
        row_temp = []

        if row:
            for column in row:
                # store only hashes and dashes
                if column == '#' or column == '-':
                    row_temp.append(column)
            maze.append(row_temp)

        start, end = get_start_end(maze)
    return maze, start, end


def get_start_end(maze):
    """
    Searches and retrieves the position of the starting and ending
    point of the given maze.

    Args:
        maze    (list): Contains the maze

    Returns:
        start  (tuple): Position of the start Node
        end    (tuple): Position of the end Node
    """

    c = 0
    for each in maze[0]:
        if each == '-':
            start = (0, c)
            c = 0
            break
        c += 1
    for each in maze[len(maze) - 1]:
        if each == '-':
            end = (len(maze) - 1, c)
        c += 1
    return start, end


def draw(maze, path, visited, file_name, walls=False):
    """
        Uses PyGame to draw and return a visualization
        of the search algorithm's pathing and searched nodes.

        Parameters:
            :param maze       : Array, contains the maze, should be the return
                                value of read_maze(filename). Used in print wall
                                operations
            :param path       : Array, contains the complete traversed path from the
                                start to the end node of the maze
            :param visited    : set(), contains a list of visited nodes
            :param file_name  : str, file name of choice for the visualization image
                                Saved in visuals/ directory in workspace
            :param walls      : Bool, whether the walls should be printed or not
    """

    # get the actual size of the mazes
    og_rows = len(maze)
    og_cols = len(maze[0])

    # scale of the canvas
    scale = 2

    # set canvas size and display
    size = (width, height) = og_cols * scale, og_rows * scale
    pygame.init()
    win = pygame.display.set_mode(size, flags=pygame.HIDDEN)
    clock = pygame.time.Clock()

    # set background color
    win.fill((255, 255, 255))

    # draw visited, path and walls
    for each in visited:
        (r, c) = each
        pygame.draw.rect(win, (138, 216, 255), (c * scale, r * scale, scale, scale))
    for each in path:
        (r, c) = each
        pygame.draw.rect(win, (255, 0, 0), (c * scale, r * scale, scale, scale))

    if walls:
        for r, r1 in enumerate(maze):
            for c, c1 in enumerate(maze[0]):
                if maze[r][c] == '#':
                    pygame.draw.rect(win, (0, 0, 0), (c * scale, r * scale, scale, scale))
    clock.tick()
    pygame.display.flip()
    pygame.image.save(win, "visuals/"+file_name)
