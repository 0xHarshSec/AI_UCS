import heapq

# Define the dimensions of the maze
ROWS = 7
COLS = 6

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
def uniform_cost_search_with_heuristic(maze, start_row, start_col, goal_row, goal_col):
    priority_queue = []
    start_node = Node(start_row, start_col, 0, manhattan_distance(start_row, start_col, goal_row, goal_col))
    heapq.heappush(priority_queue, start_node)

    explored = [[False for _ in range(COLS)] for _ in range(ROWS)]
    level = 0

    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        current_row, current_col = current_node.row, current_node.col

        if explored[current_row][current_col]:
            continue
        explored[current_row][current_col] = True

        print(f"Level: {level}, Position: ({current_row}, {current_col}), Cost: {current_node.cost}, Heuristic: {current_node.heuristic}")

        if current_row == goal_row and current_col == goal_col:
            return current_node

        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col):
            if not explored[neighbor_row][neighbor_col] and maze[neighbor_row][neighbor_col] != 1:
                new_cost = current_node.cost + 1
                heuristic = manhattan_distance(neighbor_row, neighbor_col, goal_row, goal_col)
                neighbor_node = Node(neighbor_row, neighbor_col, new_cost, heuristic, current_node)
                heapq.heappush(priority_queue, neighbor_node)

        level += 1

    return None

# Print the path from start to goal
def print_path(node):
    if node is None:
        return
    print_path(node.parent)
    print(f"({node.row}, {node.col})", end=" ")

# Mark the path on the maze
def mark_path_on_maze(maze, node):
    while node is not None:
        maze[node.row][node.col] = 4  # Mark the path with a different number, e.g., 4
        node = node.parent

# Print the maze
def print_maze(maze):
    for row in maze:
        for cell in row:
            if cell == 4:
                print("P", end=" ")  # Path
            elif cell == 1:
                print("X", end=" ")  # Obstacle
            elif cell == 2:
                print("G", end=" ")  # Goal
            elif cell == 3:
                print("S", end=" ")  # Start
            else:
                print(".", end=" ")  # Empty space
        print()

# Example usage
if __name__ == "__main__":
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

    # Mark start and goal in the maze for visual representation
    maze[start_row][start_col] = 3
    maze[goal_row][goal_col] = 2

    result_node = uniform_cost_search_with_heuristic(maze, start_row, start_col, goal_row, goal_col)
    
    if result_node:
        print("Path found:")
        print_path(result_node)
        print()
        mark_path_on_maze(maze, result_node)
    else:
        print("No path found.")

    print("Maze with path marked:")
    print_maze(maze)
