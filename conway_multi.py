import pygame
import sys
import random

pygame.init()

GRID_SIZE = 25
CELL_SIZE = 25
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
SIDE_PANEL_WIDTH = 400
SCREEN_COLOR = (0, 0, 0)
DEFAULT_COLOR = (255, 255, 255)  # White
PLAYER_COLORS = {
    1: (255, 0, 0),  # Red
    2: (0, 0, 255),  # Blue
    3: (0, 255, 0),  # Green
    4: (255, 255, 0) # Yellow
}
BUTTON_COLOR = (100, 100, 100)   # Gray
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
SIDE_PANEL_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
FPS = 5

if len(sys.argv) > 1:
    if sys.argv[1] == "--base":
        print("[Initializing Base Mode]")
        SCREEN_COLOR = (50, 50, 50)
        DEFAULT_COLOR = (100, 100, 100)  # Gray
        PLAYER_COLORS = {
            1: (255, 75, 75),  # Red
            2: (75, 75, 255),  # Blue
            3: (75, 255, 75),  # Green
            4: (255, 255, 75) # Yellow
        }
        BUTTON_COLOR = (100, 100, 100)   # Gray
        BUTTON_HOVER_COLOR = (150, 150, 150)
        BUTTON_TEXT_COLOR = (255, 255, 255)
        SIDE_PANEL_COLOR = (50, 50, 50)
        TEXT_COLOR = (150, 150, 150)
    else:
        print("Invalid Argument - Did you mena '--base'?")
        sys.exit()

# Number of players
NUM_PLAYERS = 3 # Change this to 2, 3, or 4 as needed

# Create the screen
screen = pygame.display.set_mode((SCREEN_SIZE + SIDE_PANEL_WIDTH, SCREEN_SIZE + 120))
pygame.display.set_caption("[CONWAY]")

# Initialize the grid
# Each cell starts as 0 (default color), 1 for Player 1, etc.
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Font for text
font = pygame.font.Font(None, 24)

# Define button rects
button_rect = pygame.Rect((SCREEN_SIZE // 2 - 110, SCREEN_SIZE + 10), (100, 40))
reset_button_rect = pygame.Rect((SCREEN_SIZE // 2, SCREEN_SIZE + 10), (100, 40))

# Game state
running = True
simulating = False
player_turn = 1  # Start with Player 1
clock = pygame.time.Clock()

def count_neighbors(grid, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    counts = {i: 0 for i in range(1, NUM_PLAYERS + 1)}
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] in counts:
                counts[grid[r][c]] += 1
    return counts

def update_grid(grid):
    new_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            neighbors = count_neighbors(grid, row, col)
            total_neighbors = sum(neighbors.values())
            if grid[row][col] != 0:
                new_grid[row][col] = grid[row][col] if total_neighbors == 2 or total_neighbors == 3 else 0
            else:
                if total_neighbors == 3:
                    max_color_amount = max(neighbors.values())
                    max_color_list = [key for key, val in neighbors.items() if val == max_color_amount]
                    max_color = random.choice(max_color_list)
                    if neighbors[max_color] > 0:
                        new_grid[row][col] = max_color
    return new_grid

def draw_side_panel():
    pygame.draw.rect(screen, SIDE_PANEL_COLOR, (SCREEN_SIZE, 0, SIDE_PANEL_WIDTH, SCREEN_SIZE + 120))
    rules_title = font.render("Rules", True, TEXT_COLOR)
    screen.blit(rules_title, (SCREEN_SIZE + 10, 10))

    rules = [
        "1. Players take turns.",
        "2. Either, take cell or simulate.",
        "3. Click to take.",
        "4. Click Sim to simulate.",
        "5. No Repeat Turns (Ko).",
        "6. Win if only color after a Sim.",
        "7. Sim step rules for each cell:",
        "   - 2-3 neighbors, the cell lives.",
        "   - 3 neighbors, a cell is born.",
        "   - born to majority color of its neighbors.",
        "",
        "'For, Being and Non-Being produce each other.'",
        " - Tao Te Ching",
        "",
        "Colors:",
        
    ]
    for player, color in PLAYER_COLORS.items():
        if player <= NUM_PLAYERS:
            rules.append(f"   - Player {player}: {color}")

    y_offset = 50
    for rule in rules:
        rule_text = font.render(rule, True, TEXT_COLOR)
        screen.blit(rule_text, (SCREEN_SIZE + 10, y_offset))
        y_offset += 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if button_rect.collidepoint(mouse_x, mouse_y):
                simulating = not simulating
            elif reset_button_rect.collidepoint(mouse_x, mouse_y):
                grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                simulating = False
                player_turn = 1
            elif not simulating and mouse_x < SCREEN_SIZE and mouse_y < SCREEN_SIZE:
                # Calculate the grid position
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                # Change the cell's state based on the player's turn
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] == 0:
                    grid[row][col] = player_turn
                    player_turn = player_turn % NUM_PLAYERS + 1

    # Clear the screen
    screen.fill(SCREEN_COLOR)

    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = PLAYER_COLORS.get(grid[row][col], DEFAULT_COLOR)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, SCREEN_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Cell border

    # Draw the side panel
    draw_side_panel()

    # Draw the simulate button
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Sim" if not simulating else "Stop", True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    # Draw the reset button
    reset_button_color = BUTTON_HOVER_COLOR if reset_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, reset_button_color, reset_button_rect)
    reset_text = font.render("Reset", True, BUTTON_TEXT_COLOR)
    reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text, reset_text_rect)

    # Display the current player's turn
    turn_text = font.render(f"Player {player_turn}'s Turn", True, PLAYER_COLORS[player_turn])
    turn_text_rect = turn_text.get_rect(bottomright=(SCREEN_SIZE - 10, SCREEN_SIZE + 50))
    screen.blit(turn_text, turn_text_rect)

    # Count and display the number of grids for each player
    counts = {player: sum(row.count(player) for row in grid) for player in PLAYER_COLORS}
    y_offset = SCREEN_SIZE + 10
    for player, count in counts.items():
        if player <= NUM_PLAYERS:
            count_text = font.render(f"P{player}: {count}", True, PLAYER_COLORS[player])
            screen.blit(count_text, (10, y_offset))
            y_offset += 20

    # Update the grid if simulating
    if simulating:
        new_grid = update_grid(grid)
        if new_grid == grid or all(cell == 0 for row in grid for cell in row):  # Stop simulating if grid stops changing or is empty
            simulating = False
        grid = new_grid
        clock.tick(FPS)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
