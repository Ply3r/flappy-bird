import pygame
from random import randint

from pygame.transform import rotate

# Contants
WIDTH, HEIGHT = 700, 900
FPS = 60
GRAVITY = 5
VELOCITY = 15

# variables
score = 0
bird_rotate = 0
game_over = False

# Background variables
background_image = pygame.image.load('./images/background.png')
background_0 = pygame.transform.scale(background_image, [WIDTH, HEIGHT])
background_0_pos = [0, 0]
background_1 = pygame.transform.scale(background_image, [WIDTH, HEIGHT])
background_1_pos = [WIDTH, 0]

# BIRD variables
BIRD_X = 80
bird_position = [BIRD_X, HEIGHT//2]
bird_image = pygame.image.load('./images/flappy_bird.png')
bird = pygame.transform.scale(bird_image, [65, 50])

#birds_sprite
sprite_0 = pygame.transform.rotate(bird, -25)
sprite_1 = pygame.transform.rotate(bird, -20)
sprite_2 = pygame.transform.rotate(bird, -15)
sprite_3 = pygame.transform.rotate(bird, -10)
sprite_4 = pygame.transform.rotate(bird, -5)
sprite_5 = pygame.transform.rotate(bird, 0)
sprite_6 = pygame.transform.rotate(bird, 5)
sprite_7 = pygame.transform.rotate(bird, 10)
sprite_8 = pygame.transform.rotate(bird, 15)
sprite_9 = pygame.transform.rotate(bird, 20)
sprite_10 = pygame.transform.rotate(bird, 25)
sprites = [
    sprite_0, sprite_1, sprite_2, sprite_3,
    sprite_4, sprite_5, sprite_6, sprite_7,
    sprite_8, sprite_9, sprite_10
]

# initial_setup
WINDOW = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.font.init()

# Fonts
title = pygame.font.SysFont('Arial', 60)
middle_font = pygame.font.SysFont('Arial', 30)

def create_pipes():
    first_pos = [WIDTH - 30, 0]
    first_size = [150, randint(200, 400)]
    first = {'pos': first_pos, 'size': first_size}

    second_y = randint(200, 400)
    second_pos = [WIDTH - 30, HEIGHT - second_y]
    second_size = [150, second_y]
    second = {'pos': second_pos, 'size': second_size}

    return [first, second]


pipes = create_pipes()


def move_background():
    global background_0_pos
    global background_1_pos

    background_0_pos[0] -= 2
    background_1_pos[0] -= 2

    if (background_0_pos[0] < -WIDTH):
        background_0_pos[0] = WIDTH

    if (background_1_pos[0] < -WIDTH):
        background_1_pos[0] = WIDTH


def move_pipes():
    global pipes
    x_position = pipes[0]['pos'][0]
    real_speed = (VELOCITY + ((score//30) * .1))
    pipes[0]['pos'][0] = x_position - real_speed
    pipes[1]['pos'][0] = x_position - real_speed

    if x_position + VELOCITY <= -150:
        pipes = create_pipes()


def up_animation():
    global bird
    global bird_rotate

    if bird_rotate < 5: 
        bird_rotate += 1


def down_animation():
    global bird
    global bird_rotate

    if bird_rotate > -5: 
        bird_rotate -= 1


def gravity():
    global bird_position
    height = bird_position[1]
    bird_position = [BIRD_X, height + GRAVITY]
    down_animation()


def jump():
    global bird_position
    height = bird_position[1]
    bird_position = [BIRD_X, height - 10]
    up_animation()


def check_colision():
    global game_over

    first_pos = pipes[0]['pos']
    first_size = pipes[0]['size']
    second_size = pipes[1]['size']

    if 0 <= first_pos[0] <= 140 and 0 <= bird_position[1] <= first_size[1]:
        game_over = True

    if 0 <= first_pos[0] <= 140 and HEIGHT - second_size[1] - 50 <= bird_position[1] <= HEIGHT:
        game_over = True


def check_game_over():
    global game_over
    if bird_position[1] <= 0:
        game_over = True
        bird_position[1] = 0

    if bird_position[1] >= HEIGHT - 50:
        game_over = True
        bird_position[1] = HEIGHT - 50


def draw_window(score):
    # bird
    if (bird_rotate == -5):
        hold = sprites[0]
    elif (bird_rotate == -4):
        hold = sprites[1]
    elif (bird_rotate == -3):
        hold = sprites[2]
    elif (bird_rotate == -2):
        hold = sprites[3]
    elif (bird_rotate == -1):
        hold = sprites[4]
    elif (bird_rotate == 0):
        hold = sprites[5]
    elif (bird_rotate == 1):
        hold = sprites[6]
    elif (bird_rotate == 2):
        hold = sprites[7]
    elif (bird_rotate == 3):
        hold = sprites[8]
    elif (bird_rotate == 4):
        hold = sprites[9]
    else:
        hold = sprites[10]

    # Texts
    game_over_text = title.render('Game Over', False, [255, 255, 255])
    score_text = middle_font.render(f'Distance: {score//30}', False, [255, 255, 255])

    # Pipes
    first_pipe_pos = pipes[0]['pos']
    first_pipe_size = pipes[0]['size']
    first_pipe = pygame.image.load('./images/pipes.png')
    first_pipe = pygame.transform.scale(first_pipe, first_pipe_size)
    first_pipe = pygame.transform.rotate(first_pipe, 180)

    second_pipe_pos = pipes[1]['pos']
    second_pipe_size = pipes[1]['size']
    second_pipe = pygame.image.load('./images/pipes.png')
    second_pipe = pygame.transform.scale(second_pipe, second_pipe_size)

    # render itens
    if game_over:
        WINDOW.blit(background_0, background_0_pos)
        WINDOW.blit(background_1, background_1_pos)
        WINDOW.blit(game_over_text, [WIDTH//2 - 165, HEIGHT//2 - 80])
        WINDOW.blit(score_text, [WIDTH//2 - 90, HEIGHT//2 + 50])

    else:
        WINDOW.blit(background_0, background_0_pos)
        WINDOW.blit(background_1, background_1_pos)
        WINDOW.blit(first_pipe, first_pipe_pos)
        WINDOW.blit(second_pipe, second_pipe_pos)
        WINDOW.blit(hold, bird_position)
        WINDOW.blit(score_text, [0, 0])

    pygame.display.update()


def restart():
    global score
    global bird_position
    global game_over
    global pipes

    key_pressed = pygame.key.get_pressed()
    if game_over and key_pressed[pygame.K_r]:
        game_over = False
        score = 0
        bird_position = [BIRD_X, HEIGHT//2]
        pipes = create_pipes()



def game_start():
    clock = pygame.time.Clock()

    global bird_position
    global score

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not game_over:
            jump()
        else:
            gravity()

        if not game_over:
            move_background()
            move_pipes()
            score += 1
        else:
            restart()

            

        check_game_over()
        check_colision()

        draw_window(score)

    pygame.quit()


game_start()
