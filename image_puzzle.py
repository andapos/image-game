import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = 600
FONT_SIZE = 32
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 120
IMAGE_PATH = '/Users/aca/Documents/Projects/image-game/test_photo.jpg'  # Update this path to your image file

# Set up display
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + BUTTON_HEIGHT))
pygame.display.set_caption('Image Puzzle')

# Set up font
font = pygame.font.Font(None, FONT_SIZE)

# Function to get grid size
def get_grid_size():
    input_active = True
    user_input = ''

    while input_active:
        screen.fill((0, 0, 0))
        prompt_text = font.render("Enter grid size (2-10) and press Enter:", True, (255, 255, 255))
        input_text = font.render(user_input, True, (255, 255, 255))
        
        screen.blit(prompt_text, (50, 150))
        screen.blit(input_text, (50, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit() and 2 <= int(user_input) <= 10:
                        input_active = False
                        return int(user_input)
                    else:
                        user_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if len(user_input) < 2 and event.unicode.isdigit():  # Limit input to 2 digits
                        user_input += event.unicode

GRID_SIZE = get_grid_size()

TILE_SIZE = SCREEN_SIZE // GRID_SIZE

# Load and scale image
image = pygame.image.load(IMAGE_PATH)
image = pygame.transform.scale(image, (SCREEN_SIZE, SCREEN_SIZE))

# Create grid and shuffle it
grid = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
original_grid = grid[:]
random.shuffle(grid)
initial_grid = grid[:]

# Function to draw the grid
def draw_grid():
    for i, (x, y) in enumerate(grid):
        img_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        dest_rect = pygame.Rect((i % GRID_SIZE) * TILE_SIZE, (i // GRID_SIZE) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(image, dest_rect, img_rect)

# Function to draw the refresh button
def draw_button():
    button_rect = pygame.Rect((SCREEN_SIZE - BUTTON_WIDTH) // 2, SCREEN_SIZE + (BUTTON_HEIGHT - FONT_SIZE) // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    button_text = font.render("Refresh", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)
    return button_rect

# Function to swap tiles
def swap_tiles(tile1, tile2):
    idx1 = grid.index(tile1)
    idx2 = grid.index(tile2)
    grid[idx1], grid[idx2] = grid[idx2], grid[idx1]
    print_grid()

# Function to print the grid as a matrix
def print_grid():
    matrix = [[''] * GRID_SIZE for _ in range(GRID_SIZE)]
    for idx, (x, y) in enumerate(grid):
        matrix[idx // GRID_SIZE][idx % GRID_SIZE] = f'({x},{y})'
    for row in matrix:
        print(' '.join(row))
    print()  # Blank line for better readability

# Initial grid print
print("Initial grid:")
print_grid()

# Main game loop
running = True
selected_tile = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if the refresh button is clicked
            button_rect = draw_button()
            if button_rect.collidepoint(mouse_x, mouse_y):
                grid = initial_grid[:]
                random.shuffle(grid)
                print("Grid reset.")
                print_grid()
                continue  # Skip the rest of the loop to avoid unintended tile swap

            clicked_tile = None

            # Iterate through the grid to find which tile is at the clicked position
            for idx, (x, y) in enumerate(grid):
                if (mouse_x >= idx % GRID_SIZE * TILE_SIZE and mouse_x < (idx % GRID_SIZE + 1) * TILE_SIZE) and \
                   (mouse_y >= idx // GRID_SIZE * TILE_SIZE and mouse_y < (idx // GRID_SIZE + 1) * TILE_SIZE):
                    clicked_tile = (x, y)
                    break

            if clicked_tile:
                if selected_tile is None:
                    selected_tile = clicked_tile
                else:
                    swap_tiles(selected_tile, clicked_tile)
                    selected_tile = None

    screen.fill((0, 0, 0))
    draw_grid()
    draw_button()
    pygame.display.flip()

pygame.quit()
