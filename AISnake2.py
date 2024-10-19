import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
screen_width = 800
screen_height = 600

# Create the Game Window
dis = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

# Load Graphics
snake_sprites = [pygame.image.load(f'assets/snake_{i}.png') for i in range(1, 6)]
food_sprites = [pygame.image.load(f'assets/food_{i}.png') for i in range(1, 6)]
bg_images = [pygame.image.load(f'assets/bg_{i}.png') for i in range(1, 6)]

# Default Choices
current_snake_sprite = 0
current_food_sprite = 0
current_bg = 0

# Snake Block Size
snake_block = 20
snake_speed = 10

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Functions
def score_display(score):
    value = score_font.render(f"Your Score: {score}", True, (255, 255, 102))
    dis.blit(value, [0, 0])

def draw_snake(snake_list):
    for segment in snake_list:
        dis.blit(snake_sprites[current_snake_sprite], (segment[0], segment[1]))

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [screen_width / 6, screen_height / 3 + y_offset])

def draw_background():
    dis.blit(bg_images[current_bg], (0, 0))

def main_menu():
    menu = True
    while menu:
        draw_background()
        message("Welcome to Snake Game!", (255, 255, 255), -50)
        message("Press S to Start Game, O for Options, Q to Quit", (255, 255, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    gameLoop()
                elif event.key == pygame.K_o:
                    options_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def options_menu():
    global current_snake_sprite, current_food_sprite, current_bg
    menu = True
    while menu:
        draw_background()
        message("Options Menu", (255, 255, 255), -50)
        message("Press 1-5 to select Snake Sprite", (255, 255, 255), -10)
        message("Press A-E to select Food Sprite", (255, 255, 255), 20)
        message("Press F-J to select Background", (255, 255, 255), 50)
        message("Press M to return to Main Menu", (255, 255, 255), 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    current_snake_sprite = int(event.unicode) - 1
                elif event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e]:
                    current_food_sprite = ord(event.unicode) - ord('a')
                elif event.key in [pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j]:
                    current_bg = ord(event.unicode) - ord('f')
                elif event.key == pygame.K_m:
                    main_menu()

def pause_game():
    paused = True
    while paused:
        draw_background()
        message("Paused - Press C to Continue, M for Main Menu, Q to Quit", (255, 0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_m:
                    main_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def gameLoop():
    global snake_speed
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close:
            draw_background()
            message("You Lost! Press C-Play Again or M-Main Menu", (213, 50, 80))
            score_display(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_m:
                        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game()

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        draw_background()
        dis.blit(food_sprites[current_food_sprite], (foodx, foody))

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        score_display(length_of_snake - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
            length_of_snake += 1
            if length_of_snake % 5 == 0:
                snake_speed += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run Game
main_menu()