# Armin.mag
import sys
import random
from tkinter import CENTER
import pygame
import time
# START PYGAME MODULES
pygame.init()

# ALL VARIABLE
display_wight = 576
display_height = 1024
base_x = 0 
gravity = 0.25
bird_movment = 0
pipe_list = []
game_ststus = True
bird_list_index = 0
game_font = pygame.font.Font('asets/font/Flappy.TTF', 50)
score = 0
high_score = 0
active_score = True

# TYMER
create_flap = pygame.USEREVENT + 1 
pygame.time.set_timer(create_flap, 200)
create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1200)
# --------- #
win_sound = pygame.mixer.Sound('asets/sound/smb_stomp.wav')
game_over_sound = pygame.mixer.Sound('asets/sound/smb_mariodie.wav')
# --------- #
background_image = pygame.transform.scale2x(pygame.image.load('asets/sprites/background-night.png') )
base_image = pygame.transform.scale2x(pygame.image.load('asets/sprites/base.png'))
pipe_image = pygame.transform.scale2x(pygame.image.load('asets/sprites/pipe-green.png'))
bird_image_down = pygame.transform.scale2x(pygame.image.load('asets/sprites/bluebird-downflap.png'))
bird_image_mid = pygame.transform.scale2x(pygame.image.load('asets/sprites/bluebird-midflap.png'))
bird_image_up = pygame.transform.scale2x(pygame.image.load('asets/sprites/bluebird-upflap.png'))
bird_list = [bird_image_down, bird_image_mid , bird_image_up]
bird_image = bird_list[bird_list_index]
game_over = pygame.transform.scale2x(pygame.image.load('asets/sprites/message.png'))
game_over_rect = game_over.get_rect(center=(288, 600))
# --------- #
# ICON #
gameicon = pygame.image.load('asets/sprites/redbird-upflap.png')
pygame.display.set_icon(gameicon)
# WINDOW #
pygame.display.set_caption("flapy bird")


def generate_pipe_rect():
    random_pipe = random.randrange(350, 800)
    pipe_rect_top = pipe_image.get_rect(midbottom=(576, random_pipe - 300))
    pipe_rect_bottom = pipe_image.get_rect(midtop=(576, random_pipe))
    return pipe_rect_bottom, pipe_rect_top


def pipe_move_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]    
    return inside_pipes


def display_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1000:
            main_screen.blit(pipe_image, pipe)
        else:
            reversed_pipes = pygame.transform.flip(pipe_image, False, True)
            main_screen.blit(reversed_pipes, pipe)    


def check_collision(pipes):
    for pipe in pipes:
        if bird_image_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(2)
            active_score = True
            return False
        if bird_image_rect.top <= -50 or bird_image_rect.bottom >= 900:
            game_over_sound.play()
            time.sleep(2)
            active_score = False
            return False
    return True


def bird_animition():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_image_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(288, 100))
        main_screen.blit(text1, text1_rect)
    if status == 'game_over':
        # SCORE
        text1 = game_font.render(F'Score : {score}', True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(288, 100))
        main_screen.blit(text1, text1_rect)
        # HIGH SCORE
        text2 = game_font.render(F'HighScore : {high_score}', True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(288, 250))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                win_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        high_score = score

    return high_score



bird_image_rect = bird_image.get_rect(center=(100, 450))
# GAME DISPLAY
main_screen = pygame.display.set_mode((display_wight, display_height))

# GAME TIMER
clock = pygame.time.Clock()

# GAME LOGIC
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODELES
            pygame.quit()
            # TERMINATE PROGRAM
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movment = 0
                bird_movment -= 6
            if event.key == pygame.K_r and game_ststus == False:
                game_ststus = True
                pipe_list.clear()
                bird_image_rect.center = (100, 450)
                bird_movment = 0
                score = 0  

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0 

            bird_image, bird_image_rect = bird_animition() 

    # DISPLAY BACKGROUND-NIGHT.PNG      
    main_screen.blit(background_image, (0, 0))

    if game_ststus:
    
        # DISPLAYE PIPES
        pipe_list = pipe_move_rect(pipe_list)
        display_pipe(pipe_list)
        # DISPLAY BIRD IMAGE
        main_screen.blit(bird_image, bird_image_rect)
        # CHECK FOR COLLISION 
        game_ststus = check_collision(pipe_list)
        # BASE GRAVITY AND MOVMENT
        bird_movment += gravity
        bird_image_rect.centery += bird_movment
        # SHOW SCORE
        update_score()
        display_score('active')
    else:
        main_screen.blit(game_over, game_over_rect)  
        display_score('game_over')
        time.sleep(3) 
        
    # DISPLAY BASE.PNG    
    base_x -= 1
    main_screen.blit(base_image, (base_x, 850))
    main_screen.blit(base_image, (base_x + 576, 850))
    if base_x <= -576:
        base_x = 0    
    
    pygame.display.update()
    # SET GAME SPEED
    clock.tick(95)        