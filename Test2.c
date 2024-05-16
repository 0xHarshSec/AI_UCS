#include <stdio.h>
#include <stdlib.h>

// Define the dimensions of the maze
#define ROWS 7
#define COLS 6

// Node structure to represent a position in the maze
typedef struct Node {
    int row, col;
    int cost;
    struct Node* parent;
} Node;

// Create a new node
Node* create_node(int row, int col, int cost, Node* parent) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->row = row;
    new_node->col = col;
    new_node->cost = cost;
    new_node->parent = parent;
    return new_node;
}

// Check if a position is within the bounds of the maze
int is_within_bounds(int row, int col) {
    return row >= 0 && row < ROWS && col >= 0 && col < COLS;
}

// Get neighbors of a given position
void get_neighbors(int row, int col, int neighbors[][2], int* count) {
    int directions[4][2] = { {-1, 0}, {0, -1}, {0, 1}, {1, 0} }; // west, north, east, south
    *count = 0;
    for (int i = 0; i < 4; i++) {
        int new_row = row + directions[i][0];
        int new_col = col + directions[i][1];
        if (is_within_bounds(new_row, new_col)) {
            neighbors[*count][0] = new_row;
            neighbors[*count][1] = new_col;
            (*count)++;
        }
    }
}

// Uniform Cost Search algorithm
Node* uniform_cost_search(int maze[ROWS][COLS], int start_row, int start_col, int goal_row, int goal_col) {
    Node* priority_queue[1000];
    int pq_size = 0;

    Node* start_node = create_node(start_row, start_col, 0, NULL);
    priority_queue[pq_size++] = start_node;

    int explored[ROWS][COLS] = { 0 };
    int level = 0;

    while (pq_size > 0) {
        Node* current_node = priority_queue[0];
        int current_index = 0;
        for (int i = 1; i < pq_size; i++) {
            if (priority_queue[i]->cost < current_node->cost) {
                current_node = priority_queue[i];
                current_index = i;
            }
        }

        for (int i = current_index; i < pq_size - 1; i++) {
            priority_queue[i] = priority_queue[i + 1];
        }
        pq_size--;

        int current_row = current_node->row;
        int current_col = current_node->col;

        if (explored[current_row][current_col]) {
            continue;
        }
        explored[current_row][current_col] = 1;

        printf("Level: %d, Position: (%d, %d), Cost: %d\n", level, current_row, current_col, current_node->cost);

        if (current_row == goal_row && current_col == goal_col) {
            return current_node;
        }

        int neighbors[4][2];
        int count;
        get_neighbors(current_row, current_col, neighbors, &count);

        for (int i = 0; i < count; i++) {
            int neighbor_row = neighbors[i][0];
            int neighbor_col = neighbors[i][1];

            if (!explored[neighbor_row][neighbor_col] && maze[neighbor_row][neighbor_col] != 1) {
                int new_cost = current_node->cost + 1;
                Node* neighbor_node = create_node(neighbor_row, neighbor_col, new_cost, current_node);
                priority_queue[pq_size++] = neighbor_node;
            }
        }
        level++;
    }

    return NULL;
}

// Print the path from start to goal
void print_path(Node* node) {
    if (node == NULL) {
        return;
    }
    print_path(node->parent);
    printf("(%d, %d) ", node->row, node->col);
}

// Mark the path on the maze
void mark_path_on_maze(int maze[ROWS][COLS], Node* node) {
    while (node != NULL) {
        maze[node->row][node->col] = 4; // Mark the path with a different number, e.g., 4
        node = node->parent;
    }
}

// Print the maze
void print_maze(int maze[ROWS][COLS]) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            if (maze[i][j] == 4) {
                printf("P "); // Path
            } else if (maze[i][j] == 1) {
                printf("X "); // Obstacle
            } else if (maze[i][j] == 2) {
                printf("G "); // Goal
            } else if (maze[i][j] == 3) {
                printf("S "); // Start
            } else {
                printf(". "); // Empty space
            }
        }
        printf("\n");
    }
}

// Example usage
int main() {
    int maze[ROWS][COLS] = {
        {0, 0, 0, 0, 0, 2},
        {0, 0, 1, 1, 1, 1},
        {0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0},
        {1, 1, 0, 0, 1, 1},
        {3, 0, 0, 0, 0, 0}
    };

    int start_row = 6, start_col = 0;
    int goal_row = 0, goal_col = 5;

    Node* result = uniform_cost_search(maze, start_row, start_col, goal_row, goal_col);

    if (result) {
        printf("Path: ");
        print_path(result);
        printf("\n");

        mark_path_on_maze(maze, result);
        printf("Maze with path:\n");
        print_maze(maze);
    } else {
        printf("No path found.\n");
    }

    return 0;
}
