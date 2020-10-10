
from a_star_algo import AStarSearch
from visualize import Visualizer, SearchAlgo, Position, SCREEN_HEIGHT, SCREEN_WIDTH


def main():
    matrix = [[0 for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]

    
    a_star_search = AStarSearch(node_matrix=matrix, start=Position(
        10, 10), end=Position(23, 16))

    visualizer = Visualizer(search_algo=a_star_search, clock_speed=30)

    visualizer.draw_grid()
    visualizer.update()
    visualizer.run_algo()



if __name__ == '__main__':
    main()
