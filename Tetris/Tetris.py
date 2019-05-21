#############################
# #                       # #
###      PROGRAMMER:      ###
#         Kevin Cui         #
#                           #
#           DATE:           #
#         2019/05/14        #
#                           #
#          PROJECT:         #
#        Tetris arcade      #
###       game clone      ###
# #                       # #
#############################

####MODULE IMPORTS####
import pygame        # Pygame for graphics ui
import random        # Random for random generation
import os            # OS for screen moderating
import time          # Time for time display
######################

pygame.init() # Initialize pygame

UNIT = 24 # Standard unit constant

pygame.display.set_caption('Tetris')    # Set window caption
clock = pygame.time.Clock()             # Initialize frame per second object
os.environ["SDL_VIDEO_CENTERED"] = "1"  # Center window on screen

WIDTH = 30   # Standard window width constant
HEIGHT = 25  # Standard window height constant

screen = pygame.display.set_mode((WIDTH*UNIT, HEIGHT*UNIT)) # Display window

##############RGB COLOUR CONSTANTS###########
BLACK = (0, 0, 0)                           #    Base colour / Border / Text
GREY = (100, 100, 100)                      #    Base colour
WHITE = (255, 255, 255)                     # _  Text
RED = (200, 100, 100)                       #  |                 
BLUE = (100, 100, 200)                      #  |
YELLOW = (200, 200, 100)                    #   > Block colours
GREEN = (100, 200, 100)                     #  |
VIOLET = (200, 100, 200)                    # _|
#############################################

clrSelect = [RED, BLUE, YELLOW, GREEN, VIOLET] # Block colour selection list


difficulty = 1 # Initialize difficulty (level)
score = 0      # Initialize score

prev_count = 0 # Initialize previous score (for multi score bonuses)

############################################TEXT, IMAGE, AND AUDIO MEDIA######################################################################
 #--TEXT/FONTS--#
font = pygame.font.SysFont('Arial Black', 36) # Regular font
title_font = pygame.font.SysFont('Arial Black', 60) # Title font
small_font = pygame.font.SysFont('Arial Black', 14) # Small font
text = font.render("TETRIS", 5, BLACK, WHITE) # In-game title
title = font.render("TETRIS", 5, BLACK, WHITE) # Before-game title
instruct_text = small_font.render("Press any key to begin", 5, BLACK, WHITE) # Before-game instructions
end_text = font.render("Game Over", 5, BLACK, WHITE) # End-game message
 #--IMAGES--#
background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH*UNIT, HEIGHT*UNIT)).convert_alpha() # Background image
end_background = pygame.transform.scale(pygame.image.load("end_background.jpg"), (WIDTH*UNIT, HEIGHT*UNIT)).convert_alpha() # End-game image
my_face = pygame.transform.scale(pygame.image.load("me.png"), (UNIT, UNIT)).convert_alpha() # Block image
big_face = pygame.transform.scale(pygame.image.load("me.png"), (18*UNIT, 19*UNIT)).convert_alpha() # In-game on tile background image
 #--AUDIO--#
block_sound = pygame.mixer.Sound("block.wav") # Block hit obstacle sound effect
yay_sound = pygame.mixer.Sound("yay.wav") # Line cleared sound effect
###############################################################################################################################################

shapeGraphs = [ # Matrices representing block variations before rotation
    [
        [' ', 'X', ' '],      # L   X
        [' ', 'X', ' '],      #     X
        [' ', 'X', 'X']       #     X X
    ],
    [
        [' ', 'X', ' '],      # J     X
        [' ', 'X', ' '],      #       X
        ['X', 'X', ' ']       #     X X
    ],
    [
        [' ', 'X', ' '],      # Z    X
        ['X', 'X', ' '],      #    X X
        ['X', ' ', ' ']       #    X
    ],
    [
        [' ', 'X', ' '],      # S  X
        [' ', 'X', 'X'],      #    X X
        [' ', ' ', 'X']       #      X
    ],
    [
        ['X', 'X', 'X'],      # T  X X X
        [' ', 'X', ' '],      #      X
        [' ', ' ', ' ']       #
    ],
    [
        [' ', 'X', ' ', ' '], # I   X
        [' ', 'X', ' ', ' '], #     X
        [' ', 'X', ' ', ' '], #     X
        [' ', 'X', ' ', ' ']  #     X
    ],
    [
        ['X', 'X'],           # O   X X
        ['X', 'X']            #     X X
    ]]

##############MUSIC###################
pygame.mixer.music.load('theme.mp3') # Load tetris orchestral theme audio file
pygame.mixer.music.play(-1)          # Play loaded audio file
pygame.mixer.music.set_volume(0.3)   # Set volume
######################################

start_time = time.time() # Set beginning time to current computer time

                              #|---------|#
###############################| OBJECTS |##################################
                              #|---------|#                                #
#--------------------------------------------------------------------------#
class Block(object): # Single unit squared building block object           #
    def __init__(self, colour, x, y, outline): # Initialization of attributes
        self.colour = colour
        self.outline = outline
        self.x = x
        self.y = y
        self.Rect = pygame.Rect(x, y, UNIT, UNIT)

    def construct(self): # Construction of rect variable with attributes
         self.Rect = pygame.Rect(self.x, self.y, UNIT, UNIT)       
        
    def draw(self): # Draw rect
        pygame.draw.rect(screen, self.colour, self.Rect, self.outline)

    def drawImage(self): # Draw image over rect
        screen.blit(my_face, (self.x, self.y))                             #
#--------------------------------------------------------------------------#
class Cluster(object): # Block formation object                            #
    def __init__(self, colour, x, y, outline, layout): # Initialization of attributes
        self.Blocks = []
        self.colour = colour
        self.x = x
        self.y = y
        self.outline = outline
        self.layout = layout
        self.construct()

    def construct(self): # Construction of list of rect variable with attributes
        self.Blocks.clear()
        for r in range(len(self.layout)):
            for c in range(len(self.layout[r])):
                if self.layout[r][c] == 'X':
                    self.Blocks.append(Block(self.colour, self.x+r*UNIT, self.y+c*UNIT, self.outline))
                    
    def draw(self): # Draw all rects in list
        for block in self.Blocks:
            block.draw()                                                   #
#--------------------------------------------------------------------------#
class Shape(Cluster): # Falling block formation object                     #

    def rotate(self): # Rotates formation by shifting sides of matrix inwards clockwise
        n = len(self.layout)
        for x in range(n//2): 
            for y in range(x, n-x-1): 
                temp = self.layout[x][y] 
                self.layout[x][y] = self.layout[y][n-1-x] 
                self.layout[y][n-1-x] = self.layout[n-1-x][n-1-y] 
                self.layout[n-1-x][n-1-y] = self.layout[n-1-y][x]  
                self.layout[n-1-y][x] = temp

    def rotateBackwards(self): # Rotates formation by shifting sides of matrix inwards counter-clockwise
        n = len(self.layout)
        for x in range(n//2):
            for y in range(x, n-x-1):
                temp = self.layout[n-1-y][x]
                self.layout[n-1-y][x] = self.layout[n-1-x][n-1-y]
                self.layout[n-1-x][n-1-y] = self.layout[y][n-1-x]
                self.layout[y][n-1-x] = self.layout[x][y]
                self.layout[x][y] = temp

    def moveCluster(self, x, y): # Move entire cluster
        self.x += x*UNIT
        self.y += y*UNIT

    def drawImage(self): # Draw images over all rects in list
        for block in self.Blocks:
            screen.blit(my_face, (block.x, block.y))

    def getCollideList(self, otherList):
        for o in otherList:
            for b in self.Blocks:
                if b.Rect.colliderect(o.Rect):
                    return True
        return False
        
#--------------------------------------------------------------------------#
class Wall(Cluster): # Border formation (wall, floor, or ceiling)          #
    def __init__(self, colour, x, y, outline, orientation, length): # Initialization of attributes
        self.colour = colour
        self.x = x
        self.y = y
        self.outline = outline
        self.Blocks = []
        self.orientation = orientation
        self.length = length

    def construct(self): # Construction of list of rect variable with attributes
        for l in range(0, self.length):
            if self.orientation == 0:
                self.Blocks.append(Block(self.colour, self.x+l*UNIT, self.y, self.outline))
            elif self.orientation == 1:                                                           #
                self.Blocks.append(Block(self.colour, self.x, self.y+l*UNIT, self.outline))       #
###################################################################################################

###########################################################################################################################

def drawWindow(walls, floors, ceilings, obstacles, shape, nShape, shadow, score, difficulty): # Draw window during game
    screen.fill(BLACK) # Fill screen with black base colour
    screen.blit(background, (0, 0)) # Blit background
    screen.blit(text, (13*UNIT, UNIT//2)) # Blit title text
    score_text = small_font.render("Score: "+str(score), 5, BLACK, WHITE) # Render score text
    time_text = small_font.render("Time: "+str(round(time.time()-start_time, 2))+"s", 5, BLACK, WHITE) # Render time text
    if difficulty == 1.5:
        level_text = small_font.render("Level: 3", 5, BLACK, WHITE) # Render level text
    elif difficulty == 1.25:
        level_text = small_font.render("Level: 2", 5, BLACK, WHITE) # Render level text        
    else:
        level_text = small_font.render("Level: 1", 5, BLACK, WHITE) # Render level text
                                           #_
    screen.blit(score_text, (6, UNIT*5+3)) # |
    screen.blit(time_text, (6, UNIT*6+3))  #  > Blit all small texts
    screen.blit(level_text, (6, UNIT*7+3)) #_|
    pygame.draw.rect(screen, GREY, (7*UNIT, 3*UNIT, 19*UNIT, 20*UNIT)) # Blit game back black colour base
    screen.blit(big_face, (7*UNIT, 3*UNIT)) # Blit game back image
    for wall in walls: 
        wall.draw() # Draw side walls
    for lev in range(len(floors)):
        floors[lev].draw() # Draw floor
        ceilings[lev].draw() # Draw ceiling
    for obs in obstacles:
        obs.draw() # Draw obstacles
        obs.drawImage() # Draw image over obstacles
    shape.draw() # Draw current shape
    shape.drawImage() # Draw image over shape
    shadow.draw() # Draw shadow
    pygame.draw.rect(screen, WHITE, (nShape.x-UNIT, nShape.x-UNIT, 5*UNIT, 5*UNIT), 1) # Draw next shape box
    nShape.draw() # Draw next shape
    nShape.drawImage() # Draw image over next shape
    for i in range(7, WIDTH-5+2):                                                      #
        pygame.draw.line(screen, WHITE, (i*UNIT, 3*UNIT), (i*UNIT, (HEIGHT-3+1)*UNIT)) # Draw 
    for j in range(3, HEIGHT-3+2):                                                     # Grid
        pygame.draw.line(screen, WHITE, (7*UNIT, j*UNIT), ((WIDTH-5+1)*UNIT, j*UNIT))  #

def clrGenerate(currClr, nextClr, clrSelect): # Generate random colour from list
    clrSelect.remove(currClr) # Remove current colour
    currClr = nextClr # Set current colour to next colour
    nextClr = random.choice(clrSelect) # Generate next colour
    clrSelect.append(currClr) # Add current colour to list
    return currClr, nextClr

def createShape(currShapeGraph, nextShapeGraph, clrSelect, currClr, nextClr): # Create a shape
    currShape = Shape(currClr, 15*UNIT, 4*UNIT, 0, currShapeGraph) # Set current shape to layout of current shape
    nextShape = Shape(nextClr, 1*UNIT, 1*UNIT, 0, nextShapeGraph) # Set next shape to layout of next shape
    for i in range(random.randint(0, 3)):
        nextShape.rotate() # Rotate shape to a random orientation
    nextShape.construct() # Contruct the next shape
    return currShape, nextShape

def drawIntro(): # Draw intro screen
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    screen.blit(title, (13*UNIT, 9*UNIT))
    screen.blit(instruct_text, (12.3*UNIT, 16*UNIT))

def drawOutro(score): # Draw outro screen
    screen.fill(BLACK)
    screen.blit(end_background, (0, 0))
    screen.blit(end_text, (11*UNIT, 9*UNIT))
    end_score_text = small_font.render("Score: "+str(score), 5, BLACK, WHITE)
    screen.blit(end_score_text, (14*UNIT, 12*UNIT))

###########################################################################################################################

  ### = = = = = = = = = = = = = ###

    #     #    #    #####  #    #
    # # # #   # #     #    # #  #
    #  #  #  #####    #    #  # #
    #     #  #   #  #####  #    #

  ### = = = MAIN FUNCTION = = = ###
    
#######BOOLEAN FLAGS#######
intro_flag = True         # Intro
exit_flag = False         # During
outro_flag = False        # Outro
###########################

####################INITIALIZE WALL OBJECTS##################
lWalls = Wall(BLACK, 7*UNIT, 3*UNIT, 0, 1, 20) # Init left walls
lWalls.construct()                             # Construct
rWalls = Wall(BLACK, (WIDTH-5)*UNIT, 3*UNIT, 0, 1, 20) # Init right walls
rWalls.construct()                                     # Construct floors
floors = Wall(BLACK, 7*UNIT, (HEIGHT-3)*UNIT, 0, 0, 19)  # Init
floors.construct()                                       # Construct ceilings
ceilings = Wall(BLACK, 7*UNIT, 3*UNIT, 0, 0, 19) # Init
ceilings.construct()                             # Construct
obstacles = [] # Init empty obstacle list
#############################################################

currShapeGraph = '' # Initialize current layout of shape
nextShapeGraph = random.choice(shapeGraphs) # Set next layout of shape

nextClr = random.choice(clrSelect) # Set next colour
clrSelect.remove(nextClr) # Remove next colour from list
currClr = random.choice(clrSelect) # Set current colour

timeCount = 0 # Start frame count

rowCheck = [0]*18 # Initialize empty line checking list

########################INTRO##############################
while intro_flag:
    events = pygame.event.get() # Check events
    for event in events:
        if event.type == pygame.KEYDOWN: # Check key pressed to begin
            intro_flag = False
        if event.type == pygame.QUIT: # Check quit to exit
            intro_flag = False
            exit_flag = True
    
    drawIntro() # Display intro screen
    pygame.display.update()
###########################################################
    
########################IN GAME############################
while not exit_flag:

    if currShapeGraph == '': # If not current layout
        currShapeGraph = nextShapeGraph # Set current layout to next layout
        nextShapeGraph = random.choice(shapeGraphs) # Generate new random next layout
        currClr, nextClr = clrGenerate(currClr, nextClr, clrSelect) # Generate colours
        currShape, nextShape = createShape(currShapeGraph, nextShapeGraph, clrSelect, currClr, nextClr) # Create shape
        shadowShape = Shape(currClr, currShape.x, currShape.y, 4, currShapeGraph) # Create new shadow
    
    timeCount += 1 # Increase frame count

    if timeCount%(20//difficulty)==0: # If frame count reaches certain interval determined by difficulty level
        currShape.moveCluster(0, 1) # Automatically move down

    reachedBottom = False

    shadowShape = Shape(currClr, currShape.x, currShape.y, 4, currShape.layout)# Create shadow in position and orientation of shape

    while not reachedBottom: # Move shadow down until reaches a collider
        for block in shadowShape.Blocks:
            for obs in obstacles:
                if block.Rect.colliderect(obs.Rect):
                    shadowShape.moveCluster(0, -1)
                    shadowShape.construct()
                    reachedBottom = True
            for flr in floors.Blocks:
                if block.Rect.colliderect(flr.Rect):
                    shadowShape.moveCluster(0, -1)
                    shadowShape.construct()
                    reachedBottom = True
        if not reachedBottom:
            shadowShape.moveCluster(0, 1)
            shadowShape.construct()
                    
    events = pygame.event.get() # Get events
    for event in events:
        if event.type == pygame.KEYDOWN: # If key down
            collided = False
            if event.key == pygame.K_UP: # Rotate block
                currShape.rotate()
                currShape.construct()
                if currShape.getCollideList(lWalls.Blocks+rWalls.Blocks+obstacles):
                    currShape.rotateBackwards()
                    currShape.construct()
            if event.key == pygame.K_SPACE and timeCount%(20//difficulty)!=0: # Move down to bottom
                currShape.x = shadowShape.x
                currShape.y = shadowShape.y
            if event.key == pygame.K_LEFT: # Move to the left
                currShape.moveCluster(-1, 0)
                currShape.construct()
                if currShape.getCollideList(lWalls.Blocks+rWalls.Blocks+obstacles):
                    currShape.moveCluster(1, 0)
                    currShape.construct()
            if event.key == pygame.K_RIGHT: # Move to the right
                currShape.moveCluster(1, 0)
                currShape.construct()
                if currShape.getCollideList(lWalls.Blocks+rWalls.Blocks+obstacles):
                    currShape.moveCluster(-1, 0)
                    currShape.construct()
        if event.type == pygame.QUIT: # Exit game
            exit_flag = True

    isMoved = False

    for block in currShape.Blocks:
        for flr in floors.Blocks: # Check colloision with floor
            if block.Rect.colliderect(pygame.Rect(flr.x, flr.y-UNIT, UNIT, UNIT)) and not isMoved:
                currShapeGraph = ''
                for b in currShape.Blocks:
                    rowCheck[b.y//UNIT-4]+=1
                    if b.Rect.colliderect(flr.Rect):
                        currShape.moveCluster(0, -1)
                        currShape.construct()
                obstacles += currShape.Blocks
                isMoved = True
        for obs in obstacles: # Check collision with obstacles
            if block.Rect.colliderect(pygame.Rect(obs.x, obs.y-UNIT, UNIT, UNIT)) and not isMoved:
                currShapeGraph = ''
                if block.Rect.colliderect(pygame.Rect(obs.x, obs.y, UNIT, UNIT)):
                    currShape.moveCluster(0, -1)
                for b in currShape.Blocks:
                    rowCheck[b.y//UNIT-4]+=1
                    for cei in ceilings.Blocks:
                        if b.Rect.colliderect(pygame.Rect(cei.x, cei.y+UNIT, UNIT, UNIT)):
                            exit_flag = True
                            outro_flag = True
                            currShapeGraph = '0'
                if not outro_flag:
                    obstacles += currShape.Blocks
                isMoved = True
                
    count = 0

    for row in range(len(rowCheck)): # Check for filled rows
        if rowCheck[row] == 17:
            for upper in range(row, 1, -1):
                rowCheck[upper] = rowCheck[upper-1]
            count += 1
            obs = 0
            while obs<len(obstacles): # Clear filled rows
                if obstacles[obs].y == (row+4)*UNIT:
                    obstacles.pop(obs)
                    obs-=1
                elif obstacles[obs].y < (row+4)*UNIT: 
                    obstacles[obs].y += UNIT
                    obstacles[obs].construct()
                obs += 1
            row -= 1

    if count!=0: # Check if line cleared
        prev_count = count
        yay_sound.play() # Play cleared line sound effect
    elif currShapeGraph == '':
        block_sound.play() # Play block collision sound effect

    if count>=4: # Determine score
       if prev_count == 4:
            score += (count//4)*1200
       else:
            score += (count//4)*800
            score += (count%4)*100
    else:
        score += count*100

    if score >= 1000: # Determine level
        difficulty = 1.5
    elif score >= 500:
        difficulty = 1.25

    shadowShape.construct() #\ _ Constructing clusters
    currShape.construct()   #/
    
    drawWindow(lWalls.Blocks+rWalls.Blocks, floors.Blocks, ceilings.Blocks, obstacles, currShape, nextShape, shadowShape, score, difficulty) # Draw window
    clock.tick(60) # Set frames per second to 60
    pygame.display.update() # Update display

if outro_flag:
    time.sleep(2)

while outro_flag: # Outro screen
    events = pygame.event.get() # Check events
    for event in events:
        if event.type == pygame.QUIT: # Exit game
            outro_flag = False
            
    drawOutro(score) # Display end game screen
    pygame.display.update()

pygame.quit() # Quit pygame window
