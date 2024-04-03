import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 2
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
PINK = (255, 192, 203)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_WHITE = (255, 255, 255, 128)  # Semi-transparent white for the bubble box

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
# Board
board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

# Define Font
font = pygame.font.Font(None, 36)  # Use default font, size 36
 
# Functions
def draw_lines():
    # Horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, PINK, (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SPACE), 
                                 (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, PINK, (col*SQUARE_SIZE + SPACE, row*SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col*SQUARE_SIZE + SQUARE_SIZE - SPACE, row*SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, RED, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def place_figure(row, col, player):
    board[row][col] = player

def is_space_available(row, col):
    return board[row][col] == None

def is_board_full():
    return all(board[row][col] != None for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)):
        return True
    return False

def get_empty_cells():
    empty_cells = []
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == None:
                empty_cells.append((row, col))
    return empty_cells

def ai_move():
    empty_cells = get_empty_cells()
    return random.choice(empty_cells)

def game_over(message):
    font = pygame.font.SysFont(None, 30)
    text = font.render(message, True, PINK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bubble_rect_outer = text_rect.inflate(30, 30)  # Larger red bubble
    bubble_rect_inner = text_rect.inflate(20, 20)  # Smaller white bubble
    pygame.draw.rect(screen, RED, bubble_rect_outer)  # Draw red outer bubble with straight edges
    pygame.draw.rect(screen, WHITE, bubble_rect_inner)  # Draw white inner bubble
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)
    restart_game()

def restart_game():
    screen.fill(WHITE)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None
    pygame.display.update()
    time.sleep(4)  # Pause for 4 seconds before starting the game loop

# Draw Tic Tac Toe board lines and display
screen.fill(WHITE)
draw_lines()
pygame.display.update()

# Game loop
player_turn = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not is_board_full() and not check_win('X') and player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE
                if is_space_available(clicked_row, clicked_col):
                    place_figure(clicked_row, clicked_col, 'X')
                    draw_figures()
                    pygame.display.update()
                    if check_win('X'):
                        game_over("You're a star!")
                    elif is_board_full():
                        game_over("It's a tie!")
                    else:
                        player_turn = False
                        ai_thinking_text = font.render("AI is thinking...", True, BLACK)
                        screen.blit(ai_thinking_text, (10, 10))
                        pygame.display.update()
                        time.sleep(1)
        if not is_board_full() and not check_win('O') and not player_turn:
            ai_row, ai_col = ai_move()
            place_figure(ai_row, ai_col, 'O')
            draw_figures()
            pygame.display.update()
            if check_win('O'):
                game_over("Womp womp :(")
            elif is_board_full():
                game_over("It's a tie!")
            else:
                player_turn = True
                screen.fill(WHITE)
                draw_lines()
                draw_figures()
                pygame.display.update()