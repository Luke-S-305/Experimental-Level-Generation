#Importing modules needed
import pygame
import random

#Defining colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Defining classes - pg229
class Block(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, colour, width, height):
    
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
        self.rect.y -= 0 #was previously set to 1 tests are being made without movement

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
        #Resetting values each time the loop runs - experiment with putting the
        #whole movement code into the update function and swapping "player.******"
        #for "self.******"
        """
        Use the data from line 77 onwards (depth of collision)
        This will allow me to 
        """
        self.xspeed = 0
        #self.yspeed = 0 - commented out as it is resetting fall speed to 0 every update
        speed = 1

        #increasing the speed value if shift is pressed
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            speed = 2


        # get key current state - keystate polling (https://stackoverflow.com/questions/13378846/pygame-how-to-make-smoother-movements)
        keys = pygame.key.get_pressed()
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
            
#Initialising pygame
pygame.init()

#Set screen dimensions
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode([screen_width, screen_height])

#The "block list" is a list of all the block sprites. All blocks in the program are added to this list
block_list = pygame.sprite.Group()

#Another list of every sprite as well
all_sprites_list = pygame.sprite.Group()

#Another list of all players
player_list = pygame.sprite.Group()

#Creating a dirt floor
#For loop for multiple blocks
for i in range(40):
    #creating the block
    dirtBlock = Block(BLACK, 64, 64)

    #Placing blocks
    dirtBlock.rect.x = i * 64
    dirtBlock.rect.y = 640 - 64

    #Adding the block to the object lists
    block_list.add(dirtBlock)
    all_sprites_list.add(dirtBlock)

#Creating some form of player
player = Player(RED, 32, 32, 0, 0) #The 0, 0 at the end is xspeed and yspeed
player.rect.y = 0
player.rect.x = 0
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
