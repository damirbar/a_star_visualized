
from a_star_algo import AStarSearch, AStarNode
from visualize import Visualizer, SearchAlgo, Position, SCREEN_HEIGHT, SCREEN_WIDTH, Colors
import random


def main():
    matrix = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

    print(f"{len(matrix)} ROWS and {len(matrix[0])} COLUMNS")

    # start_pos = Position(random.randint(0,SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT))
    # end_pos = Position(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))


    visualizer = Visualizer(clock_speed=30)
    visualizer.draw_grid()
    visualizer.update()

    positions = visualizer.user_choose_start_end()
    print(positions)

    a_star_search = AStarSearch(node_matrix=matrix, start=positions[0], end=positions[1])

    visualizer.search_algo = a_star_search

    for i in range(7):
        pos = Position(8, i)
        node = AStarNode(pos, None)
        a_star_search.update_node_closed(node, Colors.dark_red)
    visualizer.draw_buffered_nodes()

    visualizer.run_algo()



if __name__ == '__main__':
    main()
