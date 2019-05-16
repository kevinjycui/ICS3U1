
##########################
##########################
######             #######
###### Programmer: #######
######  Kevin Cui  #######
######             #######
######    Date:    #######
######  2019-04-09 #######
######             #######
######  Clone of   #######
###### arcade game #######
######    pong     #######
######             #######
##########################
##########################

import pygame
import os
import time
import random

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"

clock = pygame.time.Clock()

pygame.display.set_caption("Pong")
window = pygame.display.set_mode((480, 360))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_dct = [-3, 3]
ver_dct = [-3, -1, 0, 1, 3]
speed_x = random.choice(_dct)
speed_y = 0

ball_x = 240
ball_y = 180
ball_radius = 10

paddle_x = [60, 420]
paddle_y = [150, 150]

RED = (200, 120, 120)
YELLOW = (200, 200, 120)
font = pygame.font.Font("msmincho.ttf", 24)

time_start = time.time()

scores = [0, 0]

def intro_screen():
    text = font.render('指示：パドルでボールを打つ', 5, RED)
    window.blit(text, (95, 100))
    pygame.display.update()

def redraw_game_field(ball, paddle_l, paddle_r):
    window.fill(BLACK)
    for scr in range(len(scores)):
        text = font.render('プレイヤー'+str(scr+1)+": "+str(scores[scr]), 5, YELLOW)
        window.blit(text, (250*(scr+1)-215, 20))
    text2 = font.render('Q', 5, YELLOW)
    window.blit(text2, (180, 140))
    text3 = font.render('A', 5, YELLOW)
    window.blit(text3, (180, 200))
    text4 = font.render('P', 5, YELLOW)
    window.blit(text4, (290, 140))
    text5 = font.render('L', 5, YELLOW)
    window.blit(text5, (290, 200))
    pygame.draw.line(window, YELLOW, (240, 55), (240, 360), 5)
    pygame.draw.line(window, WHITE, (0, 55), (480, 55), 5)
    pygame.draw.circle(window, WHITE, ball.Circle, ball_radius)
    pygame.draw.rect(window, WHITE, paddle_l.Rect)
    pygame.draw.rect(window, WHITE, paddle_r.Rect)
    pygame.display.update()
    
class Ball():
    def __init__(self):
        self.Circle = [ball_x, ball_y]

    def bounce_ball(self, paddle_l, paddle_r, speed_x, speed_y):
        if self.Circle[1] + ball_radius >= 360 or self.Circle[1] - ball_radius <= 60:
            speed_y *= -1
        if self.Circle[0] + ball_radius >= 80 and self.Circle[0] + ball_radius <= 90:
            pad = paddle_l
            width = 10 + ball_radius
        elif self.Circle[0] + ball_radius >= 420 and self.Circle[0] + ball_radius <= 430:
            pad = paddle_r
            width = 0 - ball_radius
        else:
            return speed_x, speed_y
        if self.Circle[1] + ball_radius >= pad.Rect[1] and self.Circle[1] + ball_radius < pad.Rect[1] + 15:
            speed_y *= -1
            speed_y -= 2
            speed_x *= -1
            self.Circle[0] = pad.Rect[0] + width
        elif self.Circle[1] + ball_radius >= pad.Rect[1] + 15 and self.Circle[1] + ball_radius < pad.Rect[1] + 30:            
            speed_y *= -1
            speed_y -= 1
            speed_x *= -1
            self.Circle[0] = pad.Rect[0] + width
        elif self.Circle[1] + ball_radius == pad.Rect[1] + 30:
            speed_y *= -1
            speed_x *= -1
            self.Circle[0] = pad.Rect[0] + width
        elif self.Circle[1] + ball_radius > pad.Rect[1] + 30 and self.Circle[1] + ball_radius <= pad.Rect[1] + 45:            
            speed_y *= -1
            speed_y += 1
            speed_x *= -1
            self.Circle[0] = pad.Rect[0] + width
        if self.Circle[1] + ball_radius > pad.Rect[1] + 45 and self.Circle[1] + ball_radius <= pad.Rect[1] + 60:
            speed_y *= -1
            speed_y += 2
            speed_x *= -1
            self.Circle[0] = pad.Rect[0] + width
        return speed_x, speed_y

    def move_ball(self, speed_x, speed_y):
        if self.Circle[1] + ball_radius + 1 < 480 and self.Circle[1] - ball_radius - 1 > 0:
            self.Circle[0] += speed_x
            self.Circle[1] += speed_y

    def cast_new_ball(self, paddle, lose_direct):
        self.Circle[1] = paddle.Rect[1]+30
        self.Circle[0] = paddle.Rect[0]+lose_direct+(lose_direct//abs(lose_direct))*ball_radius
        speed_x = lose_direct//abs(lose_direct)*3
        speed_y = random.choice(ver_dct)
        return speed_x, speed_y
        
class Paddle():
    def __init__(self, num):
        self.Rect = [paddle_x[num], paddle_y[num], 10, 50]

    def key_pressed(self, left):
        key = pygame.key.get_pressed()
        if key[pygame.K_q] and left:
            self.Rect[1]-=3
        if key[pygame.K_a] and left:
            self.Rect[1]+=3
        if key[pygame.K_p] and not left:
            self.Rect[1]-=3
        if key[pygame.K_l] and not left:
            self.Rect[1]+=3

        if self.Rect[1]<60:
            self.Rect[1] = 60
        elif self.Rect[1]>310:
            self.Rect[1] = 310

exit_flag = False

ball = Ball()
paddle_l = Paddle(0)
paddle_r = Paddle(1)

while time.time()-time_start<=2:
    clock.tick(60)
    intro_screen()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            time_start = time.time()-2
            exit_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            time_start = time.time()-2
            exit_flag = True

for i in range(3, -1, -1):
    window.fill(BLACK)
    if i==0:
        text = font.render('行け！', 5, RED)
        window.blit(text, (225, 100))
    else:
        text = font.render(str(i), 5, RED)
        window.blit(text, (250, 100))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit_flag = True
            break
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            exit_flag = True
            break
    time.sleep(1)

while not exit_flag:
    clock.tick(60)

    paddle_l.key_pressed(True)
    paddle_r.key_pressed(False)

    speed_x, speed_y = ball.bounce_ball(paddle_l, paddle_r, speed_x, speed_y)

    if ball.Circle[0]-ball_radius-1 >=480:
        scores[0] += 1
        speed_x, speed_y = ball.cast_new_ball(paddle_l, 10)
    elif ball.Circle[0]+ball_radius+1 <= 0:
        scores[1] += 1
        speed_x, speed_y = ball.cast_new_ball(paddle_r, -1)

    ball.move_ball(speed_x, speed_y)

    redraw_game_field(ball, paddle_l, paddle_r)

    if scores[0]==7 or scores[1]==7:
        redraw_game_field(ball, paddle_l, paddle_r)
        time.sleep(1)
        game_end_flag = False
        while not game_end_flag:
            window.fill(BLACK)
            text = font.render(str(scores[0])+":"+str(scores[1]), 5, RED)
            text2 = font.render('ゲームオーバー', 5, RED)
            window.blit(text2, (170, 100))
            window.blit(text, (230, 170))
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    game_end_flag = True
                    exit_flag = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    game_end_flag = True
                    exit_flag = True
                    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            exit_flag = True

pygame.quit()
