from utils import read_maze, draw
from a_star import astar
from depth_first import dfs
from bi_a_star import bi_a_star


if __name__ == '__main__':
    # read Maze of choice and get start, end positions
    maze, start, end = read_maze("maze-VLarge.txt")

    # call search algorithms
    d_path, d_closed = dfs(maze, start, end)
    # print(d_path)

    a_path, a_closed = astar(maze, start, end)
    # print(a_path)

    bi_path, bi_closed = bi_a_star(maze, start, end)
    # print("Bidirectional path: ", bi_path)

    # draw maze pathing, save to < file_name >
    # draw(maze, bi_path, bi_closed, "bi-a-star-VLarge.jpeg", False)
