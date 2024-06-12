import pygame
import random
import serial
import time

# Initialize Pygame
print("Initializing Pygame...")
pygame.init()
print("Pygame initialized.")

# Set up display
width, height = 300, 600
block_size = 30
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arduino Controlled Tetris")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(0, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 127, 0)]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Initialize serial communication
try:
    print("Initializing serial communication...")
    arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port
    time.sleep(2)  # Wait for the connection to be established
    print("Serial communication established.")
except serial.SerialException:
    print("Could not open serial port. Please check the port and try again.")
    exit()

# Game settings
cols = width // block_size
rows = height // block_size

def create_grid():
    return [[0 for _ in range(cols)] for _ in range(rows)]

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            color = COLORS[grid[y][x]] if grid[y][x] else BLACK
            pygame.draw.rect(window, color, (x * block_size, y * block_size, block_size, block_size), 0)
            pygame.draw.rect(window, WHITE, (x * block_size, y * block_size, block_size, block_size), 1)

def draw_shape(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(window, COLORS[shape_color], (off_x + x * block_size, off_y + y * block_size, block_size, block_size), 0)
                pygame.draw.rect(window, WHITE, (off_x + x * block_size, off_y + y * block_size, block_size, block_size), 1)

def rotate_shape(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and (
                x + off_x // block_size < 0 or
                x + off_x // block_size >= cols or
                y + off_y // block_size >= rows or
                grid[y + off_y // block_size][x + off_x // block_size]
            ):
                return True
    return False

def merge_shape(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y // block_size][x + off_x // block_size] = shape_color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_lines = rows - len(new_grid)
    new_grid = [[0 for _ in range(cols)] for _ in range(cleared_lines)] + new_grid
    grid = new_grid
    return cleared_lines

def read_arduino():
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').strip()
        print(f"Arduino command: {line}")
        return line
    return None

# Game variables
grid = create_grid()
shape = random.choice(SHAPES)
shape_color = random.randint(1, len(COLORS) - 1)
shape_pos = [cols // 2 * block_size, 0]

clock = pygame.time.Clock()
fall_time = 0
fall_speed = 500  # milliseconds

running = True
print("Starting game loop...")
while running:
    window.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if fall_time >= fall_speed:
        fall_time = 0
        shape_pos[1] += block_size
        if check_collision(shape, shape_pos):
            shape_pos[1] -= block_size
            merge_shape(shape, shape_pos)
            clear_lines()  # Clear filled rows
            shape = random.choice(SHAPES)
            shape_color = random.randint(1, len(COLORS) - 1)
            shape_pos = [cols // 2 * block_size, 0]
            if check_collision(shape, shape_pos):
                running = False  # Game over

    command = read_arduino()
    if command:
        if command == "LEFT":
            shape_pos[0] -= block_size
            if check_collision(shape, shape_pos):
                shape_pos[0] += block_size
        elif command == "RIGHT":
            shape_pos[0] += block_size
            if check_collision(shape, shape_pos):
                shape_pos[0] -= block_size
        elif command == "ROTATE":
            rotated_shape = rotate_shape(shape)
            if not check_collision(rotated_shape, shape_pos):
                shape = rotated_shape

    draw_grid()
    draw_shape(shape, shape_pos)
    pygame.display.update()

pygame.quit()
arduino.close()
print("Pygame window closed and serial connection terminated.")
