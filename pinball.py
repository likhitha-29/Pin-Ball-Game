import pygame
import sys

pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pinball Game with Lives")

# Colors
#WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK=(0,0,0)
ASH=(178, 190, 181)

# Ball properties
ball_radius = 10
ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30
ball_speed_x, ball_speed_y = 0, 0  # Ball starts stationary on the paddle

# Paddle properties
paddle_width, paddle_height = 100, 15
paddle_x, paddle_y = (SCREEN_WIDTH - paddle_width) // 2, SCREEN_HEIGHT - paddle_height
paddle_speed = 7

# Lives
lives = 3

# Game state
game_over = False
ball_started = False  # True when the ball starts moving

def draw_ball():
    pygame.draw.circle(screen, BLACK, (ball_x, ball_y), ball_radius)

def draw_paddle():
    pygame.draw.rect(screen, BLACK, (paddle_x, paddle_y, paddle_width, paddle_height))

def show_lives():
    font = pygame.font.Font(None, 36)
    text = font.render("Lives: " + str(lives), True, RED)
    screen.blit(text, (10, 10))

def show_out_message():
    font = pygame.font.Font(None, 72)
    text = font.render("Out!", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 36))

def show_restart_message():
    font = pygame.font.Font(None, 36)
    text = font.render("Press R to restart or Q to quit", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 36))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if game_over:
        if keys[pygame.K_r]:
            # Restart the game
            ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30
            ball_speed_x, ball_speed_y = 0, 0  # Ball starts stationary on the paddle
            lives = 3
            game_over = False
            ball_started = False  # Reset ball state

        elif keys[pygame.K_q]:
            # Quit the game
            pygame.quit()
            sys.exit()

    else:
        if ball_started:
            # Update ball position only if the ball has started
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball collision with walls
            if ball_x <= ball_radius or ball_x >= SCREEN_WIDTH - ball_radius:
                ball_speed_x *= -1
            if ball_y <= ball_radius:
                ball_speed_y *= -1

            # Ball collision with paddle
            if ball_y >= paddle_y - ball_radius and paddle_x <= ball_x <= paddle_x + paddle_width:
                ball_speed_y *= -1

            # Ball out of bounds (lose life)
            if ball_y >= SCREEN_HEIGHT:
                lives -= 1
                if lives > 0:
                    # Reset the ball position and velocity
                    ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30
                    ball_speed_x, ball_speed_y = 0, 0  # Ball starts stationary on the paddle
                    ball_started = False  # Reset ball state
                else:
                    # Game over: Display out message and set game_over flag
                    ball_speed_x, ball_speed_y = 0, 0
                    game_over = True

        else:
            # Ball is on the paddle, wait for the player to tap a key to start
            if any(keys):
                ball_speed_x, ball_speed_y = 3, -3  # Start ball movement
                ball_started = True

        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
            paddle_x += paddle_speed

    screen.fill(ASH)
    draw_ball()
    draw_paddle()
    show_lives()

    if game_over:
        show_out_message()
        show_restart_message()

    pygame.display.flip()
    clock.tick(60)
