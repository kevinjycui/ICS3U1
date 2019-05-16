#############################
##                         ##
##        PROGRAMMER       ##
##  --Kevin Junyang Cui--  ##
##                         ##
##           DATE          ##
##  ------2019-04-04-----  ##
##                         ##
##       DESCRIPTION       ##
##  -----Brickbreaker----  ##
##                         ##
#############################

##Import Modules##
import os        # For manipulating screen
import pygame    # For creating game
import random    # For selecting randomly generated brick colours
import math      # For logarithmic speed increase
import time      # For time delay
##################

os.environ["SDL_VIDEO_CENTERED"] = "1"          # Center screen
pygame.init()                                   # Initialize Pygame module
                                                #
pygame.display.set_caption("Brickbreaker")      # Set caption
screen = pygame.display.set_mode((640, 500))    # Display window
                                                #
clock = pygame.time.Clock()                     # Set clock for frame rate

######Ball Values######
ball_radius=10        # Radius of ball
ball_x=100            # X-position
ball_y=300            # Y-position
speed_x = 1.0         # X-speed
speed_y = 1.0         # Y-speed
outline = 0           # Ball outline set to 0 for solid ball
#######################

#####Paddle Values#####
paddle_length=125     # Horizontal length of paddle
paddle_width=25       # Vertical width of paddle
paddle_x=0            # X-position
paddle_y=465          # Y-position
#######################

BLACK = (0, 0, 0)           # Static colours
WHITE = (255, 255, 255)     #
RED = (180, 0, 0)           #
GREEN = (34, 139, 34)       #

title_font = pygame.font.SysFont("Times New Roman", 24)                                                 # Load fonts
font = pygame.font.SysFont("Times New Roman", 18)                                                       #
background = pygame.transform.scale(pygame.image.load("background.jpg"), (640, 500)).convert_alpha()    # Load images
icon = pygame.transform.scale(pygame.image.load("icon.png"), (90, 90)).convert_alpha()                  #
pygame.mixer.music.load('music.mp3')                                                                    # Load audio

score = 0                   # Set score
                            #
colours = []                # List of colours per brick
is_visible = []             # List of visibility per brick
                            #
playing = True              # Checks if game over
                            #
level = [                   # Set brick level
" X X X X",
"X X X X",
" X X X X",
"X X X X",
" X X X X",
"X X X X",
" X X X X",
"X X X X",
" X X X X",
"X X X X",
" X X X X",
"X X X X",
" X X X X",
"X X X X",
]

clr_chance = [RED, WHITE, GREEN]                            # Colour possibilities
                                                            #  
frame_count = 0                                             # Counts frames for speed increase timing
                                                            #
for row in level:                                           #
    for col in row:                                         #
        if col=='X':                                        #
            colours.append((random.choice(clr_chance)))     # Set all colours
            is_visible.append(True)                         # Set all visibility to true upon initialization

##                                 -----------------------
####-------------------------------|  DISPLAY FUNCTIONS  |-----------------------------------####
##                                 -----------------------                                     ##
                                                                                               ##
##                               Display when game is running                                  ##
                                                                                               ##
def display():                                                                                 ##
    screen.fill(BLACK)                                                                         ##
    screen.blit(background, (0, 0))                                                            ## Draw background
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius, outline)        ## Draw ball
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_length, paddle_width))         ## Draw paddle
    for row in range(len(level)):                                                              ##
        for col in range(len(level[row])):                                                     ##
            if level[row][col]=='X' and is_visible[4*row+col//2]:                              ##
                pygame.draw.rect(screen, colours[4*row+col//2], (row*50-50, col*35, 87, 30))   ## Draw bricks
    if (frame_count-start_count) % 360 <= 70 and frame_count-start_count>=360:                 ##
        text = title_font.render("FASTER", 5, WHITE)                                           ##
        pygame.draw.rect(screen, BLACK, (270, 350, 113, 50))                                   ## Draw 'faster' text box
        screen.blit(text, (285, 365))                                                          ## Draw 'faster' text
    pygame.display.update()                                                                    ##
                                                                                               ##
##-------------------------------------------------------------------------------------------####
                                                                                               ##
##                                Display when game is lost                                    ##
def lose_display():                                                                            ##
    screen.fill(BLACK)                                                                         ##
    game_over = title_font.render("GAME OVER. ARRIVEDERCI!", 5, WHITE)                         ##
    screen.blit(game_over, (160, 180))                                                         ## Draw end-game message if lost
    pygame.display.update()                                                                    ##
                                                                                               ##
##-------------------------------------------------------------------------------------------####
                                                                                               ##
##                                 Display when game is won                                    ##
def win_display():                                                                             ##
    screen.fill(BLACK)                                                                         ##
    game_over = title_font.render("YOU WIN. CONGRATULAZIONI!", 5, WHITE)                       ##
    screen.blit(game_over, (160, 180))                                                         ## Draw end-gae message if won
    pygame.display.update()                                                                    ##
                                                                                               ##
##-------------------------------------------------------------------------------------------####
                                                                                               ##
##                                   Display when at menu                                      ## 
def start_display():                                                                           ##
    screen.fill(BLACK)                                                                         ##
    game_start = title_font.render("BRICK", 5, GREEN)                                          ## 
    game_start2 = title_font.render("BREAK", 5, WHITE)                                         ##
    game_start3 = title_font.render("ITALIA", 5, RED)                                          ##
    text = font.render("[Press any key to begin]", 5, WHITE)                                   ## _
    screen.blit(game_start, (190, 120))                                                        ##  |
    screen.blit(game_start2, (290, 120))                                                       ##  > Draw title
    screen.blit(game_start3, (400, 120))                                                       ## _|
    screen.blit(text, (245, 340))                                                              ## Draw start-game message
    screen.blit(icon, (290, 200))                                                              ## Draw game icon
    pygame.display.update()                                                                    ##
                                                                                               ##
##-------------------------------------------------------------------------------------------####
##

##                                     -----------------
##-------------------------------------|      MAIN     |-------------------------------------####
##                                     -----------------                                       ##
                                                                                               ##
menu_flag = False # Start menu                                                                 ##
exit_flag = False # Start game                                                                 ##
pygame.mixer.music.play(0) # Play opening music                                                ##
                                                                                               ##
#####################                                                                          ##
#   Starting Menu   #                                                                          ##
#####################                                                                          
                                                                                               
while not menu_flag:
    clock.tick(60)
    start_display()                                                                            
    for e in pygame.event.get():                                                                  
            if e.type == pygame.QUIT: # Check if exit program                                                         
                menu_flag = True                                                               
                exit_flag = True                                                               
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:                       
                menu_flag = True                                                               
                exit_flag = True                                                               
            if e.type == pygame.KEYDOWN: # Check if key pressed                                                    
                menu_flag = True                                                               
                pygame.mixer.music.stop()                                                      
                pygame.mixer.music.load('music2.mp3') # Load game music                                         
                pygame.mixer.music.set_volume(0.3)                                             
                pygame.mixer.music.play(-1) # Play game music                                                  
                screen.fill(BLACK)                                                             
                text = font.render("Kevin Junyang Cui", 5, WHITE) # Credits                              
                screen.blit(text, (260, 260))                                                  
                pygame.display.update()                                                        
                time.sleep(3)                                                                  
                screen.fill(BLACK)                                                             
                text = font.render("Brickbreaker", 5, WHITE)                                   
                screen.blit(text, (270, 260))
                pygame.display.update()
                time.sleep(1)
                screen.fill(BLACK)
                text = font.render("Grade 11 Computer Science", 5, WHITE)
                screen.blit(text, (220, 260))
                pygame.display.update()
                time.sleep(1)
                start_count = frame_count # Check beginning frame count
                break

#################
#    In game    #
#################

while not exit_flag:
        
    clock.tick(60) # Set FPS

    frame_count += 1 # Increase frame count once per update
        
    for e in pygame.event.get():
        if e.type == pygame.QUIT: # Check if exit program
            exit_flag = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            exit_flag = True

    ball_x += speed_x # Move ball                   
    ball_y += speed_y

    if paddle_x<=640-paddle_length: # Prevent paddle from leaving screen
        paddle_x = pygame.mouse.get_pos()[0]
    if paddle_x>640-paddle_length:
        paddle_x = 640-paddle_length

    if ball_x+ball_radius> 640 or ball_x-ball_radius<0: # Bounce ball on edges
        speed_x *= -1
    if ball_y-ball_radius<0:
        speed_y *= -1
    
    if ball_y+ball_radius>=paddle_y and ball_y<=paddle_y+paddle_width and ball_x>=paddle_x and ball_x<=paddle_x+paddle_length: # Bounce ball on paddle
        if (ball_x > paddle_x+paddle_length//2 and speed_x<0) or (ball_x < paddle_x+paddle_length//2 and speed_x>0): # Check paddle side for horizontal reflection
            speed_x *= -1 
        speed_y *= -1

    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col]=='X' and is_visible[4*row+col//2] and ball_x+ball_radius>=row*50-50 and ball_x-ball_radius<=row*50-50+87 and ball_y+ball_radius>=col*35 and ball_y-ball_radius<=col*35+30:
                if (ball_x > row*50-50+87//2 and speed_x<0) or (ball_x < row*50-50+87//2 and speed_x>0): # Bounce ball on bricks ^
                    speed_x *= -1 # Check paddle side for horizontal reflection ^
                speed_y *= -1
                is_visible[4*row+col//2] = False # Set visibility of brick to False
                score += 1 # Increase score

##################
#    Game lost   #
##################

    if ball_y+ball_radius*2>510: # Check if ball fell out of window
        if playing: # If game is still playing
            pygame.mixer.music.stop()
            time.sleep(2)
            pygame.mixer.music.load('music.mp3') # Load ending music
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(0) # Play ending music
            playing = False # Set game playing to False
        lose_display() # Display losing screen
        for e in pygame.event.get():
            if e.type == pygame.QUIT: # Check if exit program
                exit_flag = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                exit_flag = True

#################
#   Game won    #
#################

    elif score >= 4*14: # Check if score is maximum
        if playing: # If game is still playing
            pygame.mixer.music.stop()
            ball_y=0
            ball_x=0
            pygame.mixer.music.load('music.mp3') # Load ending music
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(0) # Play ending music
            playing = False # Set game playing to False
        win_display() # Display winning screen
        for e in pygame.event.get():
            if e.type == pygame.QUIT: # Check if exit program
                exit_flag = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                exit_flag = True
                
###################
#   Display game  #
###################

    else:   
        display() # Display game screen       
        if (frame_count-start_count) % 360 == 0: # For every 360 frames
            speed_x+=math.log10(score)*0.1*speed_x//abs(speed_x) #\_ Increase speed logarithmically in direction of speed
            speed_y+=math.log10(score)*0.1*speed_y//abs(speed_y) #/

pygame.quit() # Quit program


    

