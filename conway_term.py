import sys
import time

# Define constants
GRID_SIZE = 10

# Initialize the grid
# Each cell starts as 0 (default), 1 for Player 1, 2 for Player 2
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Game state
player_turn = 1  # 1 for Player 1, 2 for Player 2

def count_neighbors(grid, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    counts = {1: 0, 2: 0}
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] == 1:
                counts[1] += 1
            elif grid[r][c] == 2:
                counts[2] += 1
    return counts

def update_grid(grid):
    new_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            neighbors = count_neighbors(grid, row, col)
            total_neighbors = neighbors[1] + neighbors[2]
            if grid[row][col] != 0:
                new_grid[row][col] = grid[row][col] if total_neighbors == 2 or total_neighbors == 3 else 0
            else:
                if total_neighbors == 3:
                    new_grid[row][col] = 1 if neighbors[1] > neighbors[2] else 2
    return new_grid

def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))
    print()

while True:
    print_grid(grid)
    print(f"Player {player_turn}'s Turn (1 for Player 1, 2 for Player 2)")
    print("Enter 'simulate' to start simulation, or 'reset' to reset the grid.")

    command = input("Enter row and col (e.g., 2 3): ").strip()

    if command.lower() == "simulate":
        while True:
            new_grid = update_grid(grid)
            if new_grid == grid or all(cell == 0 for row in grid for cell in row):
                print("Simulation ended. Grid stabilized or empty.")
                break
            grid = new_grid
            print_grid(grid)
            time.sleep(1)
        player_turn = 2 if player_turn == 1 else 1
        continue

    if command.lower() == "reset":
        grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        player_turn = 1
        print("Grid reset.")
        continue

    try:
        row, col = map(int, command.split())
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] == 0:
            grid[row][col] = player_turn
            player_turn = 2 if player_turn == 1 else 1
        else:
            print("Invalid input or cell already occupied.")
    except ValueError:
        print("Invalid input format. Please enter row and col as integers.")
