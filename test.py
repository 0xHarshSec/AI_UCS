import pygame
import heapq
import time

# Define the dimensions of the maze
ROWS = 7
COLS = 6
CELL_SIZE = 50
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Node class to represent a position in the maze
class Node:
    def __init__(self, row, col, cost, heuristic, parent=None):
        self.row = row
        self.col = col
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

# Check if a position is within the bounds of the maze
def is_within_bounds(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# Get neighbors of a given position
def get_neighbors(row, col):
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # west, north, east, south
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if is_within_bounds(new_row, new_col):
            neighbors.append((new_row, new_col))
    return neighbors

# Calculate Manhattan distance heuristic
def manhattan_distance(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

# Uniform Cost Search algorithm with heuristic (A*)
def uniform_cost_search_with_heuristic(maze, start_row, start_col, goal_row, goal_col, screen):
    priority_queue = []
    start_node = Node(start_row, start_col, 0, manhattan_distance(start_row, start_col, goal_row, goal_col))
    heapq.heappush(priority_queue, start_node)

    explored = [[False for _ in range(COLS)] for _ in range(ROWS)]

    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        current_row, current_col = current_node.row, current_node.col

        if explored[current_row][current_col]:
            continue
        explored[current_row][current_col] = True

        draw_maze(screen, maze, (current_row, current_col))
        pygame.display.update()

        # Introduce a delay (in milliseconds) to slow down the pathfinding process
        pygame.time.delay(500)  # Adjust the delay time as needed

        if current_row == goal_row and current_col == goal_col:
            return current_node

        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col):
            if not explored[neighbor_row][neighbor_col] and maze[neighbor_row][neighbor_col] != 1:
                new_cost = current_node.cost + 1
                heuristic = manhattan_distance(neighbor_row, neighbor_col, goal_row, goal_col)
                neighbor_node = Node(neighbor_row, neighbor_col, new_cost, heuristic, current_node)
                heapq.heappush(priority_queue, neighbor_node)

    return None

# Draw the maze
def draw_maze(screen, maze, current_pos=None):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if maze[row][col] == 1:
                color = BLACK
            elif maze[row][col] == 2:
                color = GREEN
            elif maze[row][col] == 3:
                color = RED
            elif maze[row][col] == 4:
                color = YELLOW
            if current_pos and (row, col) == current_pos:
                color = BLUE

            pygame.draw.rect(screen, color, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Mark the path on the maze
def mark_path_on_maze(maze, node):
    while node is not None:
        maze[node.row][node.col] = 4  # Mark the path with a different number, e.g., 4
        node = node.parent

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Maze Pathfinding Visualization')

def main():
    maze = [
        [0, 0, 0, 0, 0, 2],
        [0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1],
        [3, 0, 0, 0, 0, 0]
    ]

    start_row, start_col = 6, 0
    goal_row, goal_col = 0, 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_maze(screen, maze)
        pygame.display.update()

        result_node = uniform_cost_search_with_heuristic(maze, start_row, start_col, goal_row, goal_col, screen)
        
        if result_node:
            mark_path_on_maze(maze, result_node)
            draw_maze(screen, maze)
            pygame.display.update()
            break

        pygame.time.wait(5000)
        running = False

    pygame.quit()

if __name__ == "__main__":
    main()
