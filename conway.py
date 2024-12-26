import pygame
import sys
import random

pygame.init()

GRID_SIZE = 25
CELL_SIZE = 30
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
SIDE_PANEL_WIDTH = 400
SCREEN_COLOR = (0, 0, 0)
DEFAULT_COLOR = (255, 255, 255)  # White
PLAYER1_COLOR = (255, 0, 0)     # Red
PLAYER2_COLOR = (0, 0, 255)     # Blue
BUTTON_COLOR = (100, 100, 100)   # Gray
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
SIDE_PANEL_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
FPS = 5
BOT = False

if len(sys.argv) > 1:
    if sys.argv[1] == "--base":
        print("[Initializing Base Mode]")
        SCREEN_COLOR = (50, 50, 50)
        DEFAULT_COLOR = (100, 100, 100)  # Gray
        PLAYER1_COLOR = (255, 255, 255)     # White
        PLAYER2_COLOR = (0, 0, 0)     # Black
        BUTTON_COLOR = (100, 100, 100)   # Gray
        BUTTON_HOVER_COLOR = (150, 150, 150)
        BUTTON_TEXT_COLOR = (255, 255, 255)
        SIDE_PANEL_COLOR = (50, 50, 50)
        TEXT_COLOR = (150, 150, 150)
    else:
        print("Invalid Argument - Did you mena '--base'?")
        sys.exit()

screen = pygame.display.set_mode((SCREEN_SIZE + SIDE_PANEL_WIDTH, SCREEN_SIZE + 60))
pygame.display.set_caption("[CONWAY]")
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
font = pygame.font.Font(None, 24)
button_rect = pygame.Rect((SCREEN_SIZE // 2 - 110, SCREEN_SIZE + 10), (100, 40))
reset_button_rect = pygame.Rect((SCREEN_SIZE // 2, SCREEN_SIZE + 10), (100, 40))

FullScreen = False
running = True
simulating = False
player_turn = 1  # 1 for Player 1, 2 for Player 2
clock = pygame.time.Clock()

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

def draw_side_panel():
    pygame.draw.rect(screen, SIDE_PANEL_COLOR, (SCREEN_SIZE, 0, SIDE_PANEL_WIDTH, SCREEN_SIZE + 60))
    rules_title = font.render("Rules:", True, TEXT_COLOR)
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
    ]

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
                player_turn = 2 if player_turn == 1 else 1
            elif reset_button_rect.collidepoint(mouse_x, mouse_y):
                grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                simulating = False
                player_turn = 1
            elif not simulating and mouse_x < SCREEN_SIZE and mouse_y < SCREEN_SIZE:
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and grid[row][col] == 0:
                    grid[row][col] = player_turn
                    player_turn = 2 if player_turn == 1 else 1
                    if BOT and player_turn == 2:
                        locations = []
                        for r in range(GRID_SIZE):
                            for c in range(GRID_SIZE):
                                if grid[r][c] == 1:
                                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                                    for dr, dc in directions:
                                        new_r = r + dr
                                        new_c = c + dc
                                        if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE and grid[new_r][new_c] == 0:
                                            locations.append((new_r, new_c))
                        if len(locations) > 0:
                            move = random.choice(locations)
                            grid[move[0]][move[1]] = player_turn
                        else:
                            simulating = True
                        player_turn = 2 if player_turn == 1 else 1

                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f or event.key == pygame.K_ESCAPE:
                if FullScreen:
                    Ekran = pygame.display.set_mode((SCREEN_SIZE + SIDE_PANEL_WIDTH, SCREEN_SIZE + 60))
                    FullScreen = False
                else:
                    Ekran = pygame.display.set_mode((SCREEN_SIZE + SIDE_PANEL_WIDTH, SCREEN_SIZE + 60), pygame.FULLSCREEN)
                    FullScreen = True

    screen.fill(SCREEN_COLOR)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 1:
                color = PLAYER1_COLOR
            elif grid[row][col] == 2:
                color = PLAYER2_COLOR
            else:
                color = DEFAULT_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, SCREEN_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Cell border

    draw_side_panel()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Sim" if not simulating else "Stop", True, BUTTON_TEXT_COLOR)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    reset_button_color = BUTTON_HOVER_COLOR if reset_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, reset_button_color, reset_button_rect)
    reset_text = font.render("Reset", True, BUTTON_TEXT_COLOR)
    reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
    screen.blit(reset_text, reset_text_rect)

    turn_text = font.render(f"Player {player_turn}'s Turn", True, PLAYER1_COLOR if player_turn == 1 else PLAYER2_COLOR)
    turn_text_rect = turn_text.get_rect(bottomright=(SCREEN_SIZE - 10, SCREEN_SIZE + 50))
    screen.blit(turn_text, turn_text_rect)

    player1_count = sum(row.count(1) for row in grid)
    player2_count = sum(row.count(2) for row in grid)
    count_text = font.render(f"P1: {player1_count}  P2: {player2_count}", True, (255, 255, 255))
    count_text_rect = count_text.get_rect(bottomleft=(10, SCREEN_SIZE + 50))
    screen.blit(count_text, count_text_rect)

    if simulating:
        new_grid = update_grid(grid)
        if new_grid == grid or all(cell == 0 for row in grid for cell in row):  # Stop simulating if grid stops changing or is empty
            simulating = False
        grid = new_grid
        clock.tick(FPS)

    pygame.display.flip()

pygame.quit()
sys.exit()
