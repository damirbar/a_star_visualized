
from a_star_algo import AStarSearch, AStarNode
from visualize import Visualizer, SCREEN_HEIGHT, SCREEN_WIDTH, Colors

def main():
    matrix = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

    visualizer = Visualizer(clock_speed=30)
    visualizer.draw_grid()
    visualizer.update()

    positions = visualizer.user_choose_start_end()
    print(positions)

    a_star_search = AStarSearch(node_matrix=matrix, start=positions[0], end=positions[1], diagonal_allowed=True)

    visualizer.search_algo = a_star_search

    obstacles = visualizer.user_choose_obstacle()
    for pos in obstacles:
        node = AStarNode(pos, None)
        a_star_search.update_node_closed(node, Colors.dark_red)
    visualizer.draw_buffered_nodes()

    visualizer.run_algo()



if __name__ == '__main__':
    main()
