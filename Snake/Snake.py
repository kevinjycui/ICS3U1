####################
# Kevin Cui
# Snake
# 2019-04-12
####################

################
import pygame #import modules
import os
import time
import random
################

pygame.init() #initialize pygame
os.environ["SDL_VIDEO_CENTERED"] = "1" #center window

clock = pygame.time.Clock() #set clock

pygame.display.set_caption("Snake") #set caption
window = pygame.display.set_mode((480, 480)) #set window

WHITE = (255, 255, 255) #static colours
BLACK = (0, 0, 0)
BLUE = (120, 120, 200)
RED = (200, 120, 120)
YELLOW = (200, 200, 120)
ORANGE = (200, 160, 0)
GREEN = (120, 200, 120)
VIOLET = (200, 120, 200)

######################################STATIC VARIABLES#########################################
font = pygame.font.SysFont('Arial Black', 48) #static fonts and sprites
font2 = pygame.font.SysFont('Arial Black', 18)
text = font.render("GAME OVER", 5, WHITE)
text3 = font.render("SNAKE", 5, BLACK, WHITE)
text4 = font2.render("Press any key to begin", 5, BLACK, WHITE)
background = pygame.transform.scale(pygame.image.load("background.jpg"), (480, 480)).convert_alpha()
intro_back = pygame.transform.scale(pygame.image.load("intro_back.png"), (480, 480)).convert_alpha()
apple = pygame.transform.scale(pygame.image.load("fruit_img/apple.png"), (24, 24)).convert_alpha()
bad = pygame.transform.scale(pygame.image.load("fruit_img/bad.png"), (24, 24)).convert_alpha()

clr_possibl = [WHITE, BLUE, ORANGE, YELLOW, VIOLET] #colour possibilities of segments
rand_clr = WHITE
clr = [WHITE]

death_sound = pygame.mixer.Sound('noise1.wav') #static audio
eat_sound = pygame.mixer.Sound('noise2.wav')
hurt_sound = pygame.mixer.Sound('noise3.wav')
################################################################################

##################DISPLAY FUNCTIONS##################

def display_window(snake, food, poison, timer, score, digest_colour): #display
    window.fill(BLACK)
    window.blit(background, (0, 0)) #draw background
    if int(timer) <= 3: #blit timer
        text2 = font2.render("Timer: "+timer+"s", 5, RED, BLACK)
    elif int(timer) > 10:
        text2 = font2.render("Timer: "+timer+"s", 5, BLUE, BLACK) 
    else:
        text2 = font2.render("Timer: "+timer+"s", 5, WHITE, BLACK)
    text3 = font2.render("Score: "+score, 5, WHITE, BLACK)
    window.blit(text2, (24, 24)) #blit words
    window.blit(text3, (376, 24))
    pygame.draw.ellipse(window, RED, food.Rect) 
    window.blit(apple, (food.Rect[0], food.Rect[1])) #blit apple
    pygame.draw.ellipse(window, GREEN, poison.Rect)
    window.blit(bad, (poison.Rect[0], poison.Rect[1])) #blit poison
    pygame.draw.ellipse(window, clr[0], snake.Rect[0])    
    for s in range(11, len(snake.Rect)-24): #blit snake
        pygame.draw.rect(window, clr[s//(len(snake.Rect)//len(clr))], snake.Rect[s])
    for s in range(len(snake.Rect)-24, len(snake.Rect)-12):
        pygame.draw.rect(window, BLACK, snake.Rect[s])        
    pygame.draw.ellipse(window, BLACK, snake.Rect[len(snake.Rect)-1])
    for d in digest_colour: #digestion animation
        if d[1] < len(snake.Rect)-24:
            pygame.draw.rect(window, d[0], (snake.Rect[d[1]][0], snake.Rect[d[1]][1], 24, 24))
    pygame.display.update()

#---------------------------------------------------#

def intro_screen(): #intro screen
    window.fill(BLUE)
    window.blit(intro_back, (0, 0))
    window.blit(text3, (130, 120))
    window.blit(text4, (120, 220))
    pygame.display.update()

#---------------------------------------------------#
    
def game_over(score): #end game screen
    window.fill(BLACK)
    window.blit(text, (85, 120))
    if score*10>255:
        score = font.render("Score: "+str(score), 5, (0, 0, 255))        
    elif score*10<0:
        score = font.render("Score: "+str(score), 5, (255, 0, 0))
    else:
        score = font.render("Score: "+str(score), 5, (255-score*10, 0, score*10))
    window.blit(score, (135, 200))
    pygame.display.update()

#---------------------------------------------------#

##################OBJECTS##################

class Snake(object): #snake
    def __init__(self):
        self.Rect = [(240, 120, 24, 24)]*24
        self.Colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Food(object): #apple
    def __init__(self):
        self.Rect = [226, 226, 24, 24]
        self.Colour = RED

class Poison(object): #poison
    def __init__(self):
        self.Rect = [226, 346, 24, 24]
        self.Colour = GREEN

###########################################

##################MAIN##################

snake = Snake() #initialize objects
food = Food()
poison = Poison()

x = snake.Rect[0][0]
y = snake.Rect[0][1]

timer = time.time() #set timer
boost_time = 0

digest_colour = []

x_direct = 0
y_direct = 0

size = 100

exit_flag = False #set flag bools
game_flag = False
intro_flag = False

pygame.mixer.music.load('intro_music.mp3')
pygame.mixer.music.play(-1) #load and play music

while not intro_flag: #intro screen
    intro_screen()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            intro_flag = True
            exit_flag = True
            game_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            intro_flag = True
            exit_flag = True
            game_flag = True
        elif e.type == pygame.KEYDOWN:
            intro_flag = True
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music.mp3')
            pygame.mixer.music.play(-1)

            
while not exit_flag: #game start

    if x_direct==0 and y_direct==0:
        timer = time.time() #reset timer

    key = pygame.key.get_pressed() #check keys

    if key[pygame.K_LEFT] and x_direct == 0 and y%24==0: #move snake
        x_direct = -1
        y_direct = 0
    elif key[pygame.K_RIGHT] and x_direct == 0 and y%24==0:
        x_direct = 1
        y_direct = 0
    elif key[pygame.K_UP] and y_direct == 0 and x%24==0:
        y_direct = -1
        x_direct = 0
    elif key[pygame.K_DOWN] and y_direct == 0 and x%24==0:
        y_direct = 1
        x_direct = 0

    x += x_direct
    y += y_direct
        
    for s in range(len(snake.Rect)-100): #if snake too small, end game
        if pygame.Rect(snake.Rect[len(snake.Rect)-1]).colliderect(snake.Rect[s]):
            exit_flag = True

    if len(snake.Rect)<13:
        snake_mouth = len(snake.Rect)
    else:
        snake_mouth = 13
    
    if pygame.Rect(snake.Rect[len(snake.Rect)-1]).colliderect(food.Rect): #eat food
        size += 50
        eat_sound.play()
        if time.time() - timer < 3:
            boost_time = 5
        else:
            boost_time = 0
        select_flag = False
        while not select_flag: #regenerate food
            select_flag = True
            rand_x, rand_y = random.randint(0, 19)*24, random.randint(0, 19)*24
            for s in snake.Rect:
                if pygame.Rect(rand_x, rand_y, 24, 24).colliderect(pygame.Rect(s)):
                    select_flag = False
        food.Rect[0], food.Rect[1] = rand_x, rand_y
        digest_colour.append([RED, len(snake.Rect)-1])
        select_flag = False
        while not select_flag: #regenerate poison
            select_flag = True
            rand_x, rand_y = random.randint(0, 19)*24, random.randint(0, 19)*24
            for s in snake.Rect:
                if pygame.Rect(rand_x, rand_y, 24, 24).colliderect(pygame.Rect(s)):
                    select_flag = False
        poison.Rect[0], poison.Rect[1] = rand_x, rand_y
        timer = time.time() #reset time

    if pygame.Rect(snake.Rect[len(snake.Rect)-1]).colliderect(poison.Rect): #eat poison
        size -= 50
        hurt_sound.play()
        select_flag = False
        while not select_flag: #regenerate poison
            select_flag = True
            rand_x, rand_y = random.randint(0, 19)*24, random.randint(0, 19)*24
            for s in snake.Rect:
                if pygame.Rect(rand_x, rand_y, 24, 24).colliderect(pygame.Rect(s)):
                    select_flag = False
        poison.Rect[0], poison.Rect[1] = rand_x, rand_y
        digest_colour.append([GREEN, len(snake.Rect)-1])

    for d in range(len(digest_colour)): #digest animation
        if d<len(digest_colour):
            if digest_colour[d][1] > 0:
                digest_colour[d][1]-=1
            else:
                digest_colour.pop(d)

    if x<0 or x+24>480 or y<0 or y+24>480 or size<100 or time.time()-timer-boost_time > 10:
        exit_flag = True
        
    snake.Rect.append((x, y, 24, 24)) #add potential piece to snake

    if size>200: #check to add piece of snake
        if len(snake.Rect)//200 > len(clr):
            for i in range(len(snake.Rect)//200 - len(clr)):
                clr_possibl.append(rand_clr)
                rand_clr = random.choice(clr_possibl)
                clr.append(rand_clr)
                clr_possibl.remove(rand_clr)
        elif len(snake.Rect)//200 < len(clr):
            for i in range(len(clr) - len(snake.Rect)//200):
                clr.pop()
            
    if len(snake.Rect) > size: #check to remove piece of snake
        snake.Rect.pop(0)

    for e in pygame.event.get(): #check exit game
        if e.type == pygame.QUIT:
            exit_flag = True
            game_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            exit_flag = True
            game_flag = True

    display_window(snake, food, poison, str(10-round(time.time()-timer-boost_time)), str((size-100)//50), digest_colour)

if not game_flag: #check end game
    death_sound.play()
    pygame.mixer.music.stop()
    time.sleep(1)
    
while not game_flag: #end game

    game_over((size-100)//50)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            game_flag = True
            
pygame.quit()
