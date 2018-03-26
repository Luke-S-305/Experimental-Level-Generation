#Importing modules needed
import pygame
import random

#Defining colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BROWN = (139,69,19)
GRAY = (119,136,153)

#Defining functions
def randBool(chance):
    return random.random() < chance

def generateMap(mapLength, mapHeight):
    #define 2d array first - the mapHeight and mapLength must be reversed to work
    square = [[0 for x in range(mapHeight+1)] for y in range(mapLength+1)]
    #Then assign values to each
    for j in range(mapHeight):
        for i in range(mapLength):
            if i == 0 or i == mapLength-1:
                square[i][j] = "border"
            elif j == 0 or j == mapHeight-1:
                square[i][j] = "border"
            elif j <= mapHeight/4:
                square[i][j] = "air"
            else:
                #defining the chance of there being a block or air
                blockChance = 0.1
                #Defining the chance of there being dirt or a stone
                stoneChance = 0.25
                """
                This code is designed to check the blocks around it and
                see whether they are air or not. The blocks around it being
                air increases the chance of the blocks near to it becoming air.
                This is to create tunnels in the ground for the player to travel
                through.
                """

                if square[i-1][j-1] == "air" and (i-1 != -1) and (j-1 != -1):
                    blockChance += 0.15
                if square[i][j-1] == "air" and (j-1 != -1):
                    blockChance += 0.15
                if (i+1 <= mapLength) and (j-1 != -1):
                    if square[i+1][j-1] == "air":
                        blockChance += 0.15
                if square[i-1][j] == "air" and (i-1 != -1):
                    blockChance += 0.15
                if not randBool(blockChance):
                    square[i][j] = "air"
                elif randBool(stoneChance):
                    square[i][j] = "stone"
                else:
                    square[i][j] = "dirt"
                
    for j in range(mapHeight):
        for i in range(mapLength):
            if square[i][j] == "border":
                borderBlock = Block(BLACK, 64, 64,64*i,64*j)#the last 2 parameters are the (scroll) x and y placements)

                #Placing blocks - possibly redundant
                borderBlock.placementx = 64 * i
                borderBlock.placementy = 64 * j
                #CAREFUL ABOUT THIS CODE ABOVE FOR RESIZING THE WINDOW
    
                #Adding the block to the object lists
                block_list.add(borderBlock)
                all_sprites_list.add(borderBlock)
                
            elif square[i][j] == "dirt":
                dirtBlock = Block(BROWN, 64, 64,64*i,64*j)#the last 2 parameters are the (scroll) x and y placements)

                #Placing blocks - possibly redundant
                dirtBlock.placementx = 64 * i
                dirtBlock.placementy = 64 * j
                #CAREFUL ABOUT THIS CODE ABOVE FOR RESIZING THE WINDOW
    
                #Adding the block to the object lists
                block_list.add(dirtBlock)
                all_sprites_list.add(dirtBlock)

            elif square[i][j] == "stone":
                stoneBlock = Block(GRAY, 64, 64,64*i,64*j)#the last 2 parameters are the (scroll) x and y placements)

                #Placing blocks - possibly redundant
                stoneBlock.placementx = 64 * i
                stoneBlock.placementy = 64 * j
                #CAREFUL ABOUT THIS CODE ABOVE FOR RESIZING THE WINDOW
    
                #Adding the block to the object lists
                block_list.add(stoneBlock)
                all_sprites_list.add(stoneBlock)

            """  
            elif square[i][j] == "air":
                #do nothing
            """



#Defining classes - pg229
class Block(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, colour, width, height, placementx, placementy):
    
        #Calls the constructor within itself, initialising the sprite
        super().__init__()

        #Setting colours
        self.image = pygame.Surface([64,64]) #Creates a blank image
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE) #Makes white a transparent colour so the background shows

        #Drawing the shape
        pygame.draw.rect(self.image, colour, [0, 0, 64, 64])

        #Create the rectangle object which has the dimensions of the image
        #The position of the object can then be updated with rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        #this will be put in the main loop and run once every second
        #the code for placing a block using scrollx is "currentscrollx + blocksize * integer(which is multiplied by blocksize to give position)
        self.rect.x = scrollx + self.placementx #placementx is where it is placed
        self.rect.y = scrolly + self.placementy #placementy is where it is placed
        
class Player(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, colour, width, height, xspeed, yspeed):
    
        #Calls the constructor within itself, initialising the sprite
        super().__init__()

        #Setting colours
        self.image = pygame.Surface([64,64]) #Creates a blank image, the actual hitbpx
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE) #Makes white a transparent colour so the background shows

        #test setup for xspeed
        self.xspeed = 0
        self.yspeed = 0
        
        #Drawing the shape
        pygame.draw.ellipse(self.image, colour, [0, 0, 64, 64]) #he visual image

        #Create the rectangle object which has the dimensions of the image
        #The position of the object can then be updated with rect.x and rect.y
        self.rect = self.image.get_rect()

    def update(self):
        """
        Try implementing this collision code
        https://stackoverflow.com/questions/44721130/pygame-collision-detection-with-walls
        """
        self.xspeed = 0
        #self.yspeed = 0 - commented out as it is resetting fall speed to 0 every update
        speed = 1

        #increasing the speed value if shift is pressed
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            speed = 2


        # get key current state - keystate polling (https://stackoverflow.com/questions/13378846/pygame-how-to-make-smoother-movements)
        keys = pygame.key.get_pressed()
        global scrollx
        global scrolly

        if keys[pygame.K_LEFT]:
            scrollx += 5
        if keys[pygame.K_RIGHT]:
            scrollx += -5
        if keys[pygame.K_UP]:
            scrolly += 5
        if keys[pygame.K_DOWN]:
            scrolly += -5

        if not blocks_hit_list: #check whether "blocks_hit_list" the list of collisions is empty
            scrolly += -1 * gravity
        
        """ - commented out for the time being
        if keys[pygame.K_LEFT]:
            self.xspeed = -1
        if keys[pygame.K_RIGHT]:
            self.xspeed = 1
        if keys[pygame.K_UP]:
            if blocks_hit_list:
                self.yspeed -= 3
            else:
                self.yspeed += 0.1
            #self.yspeed = -1
        if keys[pygame.K_DOWN]:
            self.yspeed = 1

        #move x position by xspeed
        self.rect.x += self.xspeed * speed
        #move y position by yspeed
        print(self.yspeed)
        self.rect.y += self.yspeed
        if not blocks_hit_list: #check whether "blocks_hit_list" the list of collisions is empty
            self.yspeed += 0.4 * gravity
            #note that if yspeed is negative (object falling) change to the falling sprite
        
        #if there is a collision with a block, stop falling
        elif blocks_hit_list:
            #only set yspeed to 0 if the object is falling
            if self.yspeed > 0:
                self.yspeed = 0
        """
        
#Initialising pygame
pygame.init()

#Set screen dimensions
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode([screen_width, screen_height])

#defining some variables
global scrollx
scrollx = 0
global scrolly
scrolly = 0

#The "block list" is a list of all the block sprites. All blocks in the program are added to this list
block_list = pygame.sprite.Group()

#Another list of every sprite as well
all_sprites_list = pygame.sprite.Group()

#Another list of all players
player_list = pygame.sprite.Group()

#Creating a dirt floor
#For loop for multiple blocks
generateMap(80,80)
"""
for i in range(20):
    #creating the block
    dirtBlock = Block(BLACK, 64, 64,64*i, 0)#the last 2 parameters are the (scroll) x and y placements)

    #Placing blocks
    dirtBlock.placementx = 64 * i
    dirtBlock.placementy = screen_height - 64 #this puts the blocks just above the bottom of the screen
    #CAREFUL ABOUT THIS CODE ABOVE FOR RESIZING THE WINDOW

    #Adding the block to the object lists
    block_list.add(dirtBlock)
    all_sprites_list.add(dirtBlock)
"""
#Creating some form of player
player = Player(RED, 32, 32, 0, 0) #The 0, 0 at the end is xspeed and yspeed
#placing the player in the middle of the screen
player.rect.y = screen_height/2 - 32
player.rect.x = screen_width/2 - 32
player_list.add(player)
all_sprites_list.add(player)

#setting gravity
gravity = 1

#Loop until closed
done = False

#Setting screen update speed
clock = pygame.time.Clock()
score = 0

#-----Main program loop-----
while not done:
    for event in pygame.event.get():
        #Adding events including keypresses
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    #clear screen
    screen.fill(WHITE)

    #detecting collisions
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False) #The boolean at the end is a "dokill". it determines whether the sprite is destroyes

    """ - commented out as blocks are no longer removed on collisions
    #log actual collisions in the form of score
    for dirtBlock in blocks_hit_list: #Goes through all of the dirt blocks which are touching the player
        score +=1 #add one for each block
        print("Score: ", score)
    """
        
    #update sprites
    block_list.update()
    player_list.update()
    
    #Draw sprites
    all_sprites_list.draw(screen)

    #Set framerate to 60fps
    clock.tick(60)

    #Flip screen and update
    pygame.display.flip()

#Closes program when the loop finishes
pygame.quit()
