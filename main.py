"""
 Born Underground
 Platforming Game

 Written by Tom Burrows
 Jan-July 2016

 Originally based off platforming example:
 http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
"""

import pygame
import random

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 200)
ORANGE = (255, 80, 0)
GRAY = (170, 170, 170)
YELLOW = (170, 50, 50)

SCREEN_WIDTH = 1280 # 40 blocks x 32 pixels
SCREEN_HEIGHT = 640 # 20 blocks x 32 pixels
HALF_SCREEN_WIDTH = SCREEN_WIDTH/2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT/2
'''
def gameover():
    reset = False
    global over
    global done
    textGO = fontGO.render("GAME OVER", True, ORANGE)
    screen.blit(textGO, [100, 150])
    pygame.display.flip()
    while reset == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset = True
                done = True
                over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reset = True
                        done = True

'''

class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, skin):
        super().__init__()
        '''
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(GREEN)
        '''
        self.image = skin
        # self.rect is just the variable, Rect command creates a pygame object for storing rectangular co-ordinates                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              )
        self.rect = pygame.Rect(x, y, self.width, self.height)

class SemiPlatform(Platform):
    # Platform that can be passed through from the bottom, but can be stood on
    def __init__(self, x, y, skin):
        self.width = 32
        self.height = 1
        super().__init__(x,y,skin)

class SolidPlatform(Platform):
    # Normal platform
    def __init__(self,x,y,skin):
        self.width = 32
        self.height = 32
        super().__init__(x,y,skin)
            

class MovingPlatform(SolidPlatform):
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    level = None



    def update(self):
        #print("LOL")
        #print("HEHE")
        ''' Move the platform.
            If the player is in the way, it will shove the player
            out of the way.
        '''
        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:

            # We did hit the player. Shove the player around and assume he won't hit anything else.

            # If player is moving right, set player's right side to the left side of the item player hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right



        # Move up/down
        self.rect.y += self.change_y

        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check boundaries and see if we need to reverse direction
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        if self.rect.right > self.boundary_right or self.rect.left < self.boundary_left:
            self.change_x *= -1

    def movplatsetdir(self):
        # Set direction
        if self.change_x > 0:
            self.direction = "R"
        elif self.change_x < 0:
            self.direction = "L"
        else:
            self.direction = "N"




class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        if self.status == "player":
            self.image = dwarfR
            self.image.set_colorkey(WHITE)

        elif self.status == "enemy":
            self.image = enemy1R
            self.image.set_colorkey(WHITE)
        else:
            # Create an image of the block, and fill it with a color.
            # this could also be an image laoded from the disk.
            self.image = pygame.Surface([self.width,self.height])
            self.image.fill(self.color)

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Set the start position
        self.rect.x = self.startx
        self.rect.y = self.starty

        # Set speed vector of player
        self.change_x = self.startvelocity
        self.change_y = 0

        # List of sprites we can bump against
        self.level = None


    def update(self):
        """ Move the player. """

        # Set direction
        self.setdir()

        # Change picture
        self.flippic()

        #Gravity
        self.calc_grav()

        if self.falltype == False:
            self.changedirectionatedges()

        
        # Move up/down
        self.rect.y += self.change_y
        
        
        # See if we hit anything up/down
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if type(block) == SemiPlatform:
                # Check if moving down and our feet are higher than their top
                # so we are actually supposed to be moved up. Allows for increased velocity
                if self.change_y > 0 and self.rect.bottom - 1 - self.change_y < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0

                
            else: # (if block != SemiPlatform)
                if self.change_y < 0: # Travelling up
                    self.rect.top = block.rect.bottom
                elif self.change_y > 0: # Travelling down
                    self.rect.bottom = block.rect.top
            

                self.change_y = 0

            # Move with moving platform
            if isinstance(block, MovingPlatform) and self.change_y >= 0:
                self.rect.x += block.change_x
                # Set our direction to moving platform's direction
                if self.direction == "N":
                    block.movplatsetdir()
                    self.direction = block.direction


        
        # Move left/right
        self.rect.x += self.change_x
        
        # See if we hit anything sideways
        # Do it twice; once for moving platforms, then for still
        #block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for i in range(2):
            if i == 0:
                block_hit_list = pygame.sprite.spritecollide(self, self.level.moving_platform_list, False)
            elif i == 1:
                block_hit_list = pygame.sprite.spritecollide(self, self.level.still_platform_list, False)



            for block in block_hit_list:
                if type(block) != SemiPlatform:

                    # If we are moving right,
                    # set our right side to the left side of the item we hit
                    if self.direction == "R":
                        self.rect.right = block.rect.left


                    elif self.direction == "L":
                        # Otherwise if we are moving left, do the opposite
                        self.rect.left = block.rect.right

                    elif self.direction == "N":
                        print("ERROR: DIRECTION IS N")

                    else:
                        print("ERROR: ELSE")

                    # If we are an enemy, change direction
                    if self.status == "enemy":
                        if self.status == "enemy" and self.falltype == True:
                            self.enemyjump()
                        else:
                            self.change_x *= -1
                

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .40 #ADJUST GRAVITY HERE

    def flippic(self):
        # Flips picture if facing different direction
        if self.status == "player":
            if self.direction == "R":
                self.image = dwarfR
            elif self.direction == "L":
                self.image = dwarfL
        if self.status == "enemy":
            if self.direction == "R":
                self.image = enemy1R
            elif self.direction == "L":
                self.image = enemy1L
        self.image.set_colorkey(WHITE)

    def setdir(self):
    # Set direction
        if self.change_x > 0:
            self.direction = "R"
        elif self.change_x < 0:
            self.direction = "L"
        else:
            self.direction = "N"

    def enemyjump(self):

        # Check if on ground
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0:

            # Move a blocks width up and across, then check if hitting a block
            self.rect.y -= 32

            if self.direction == "R":
                self.rect.x += 32
            if self.direction == "L":
                self.rect.x -= 32

            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

            # Move back
            self.rect.y += 32

            if self.direction == "R":
                self.rect.x -= 32
            if self.direction == "L":
                self.rect.x += 32

            # If not hitting block, jump.
            # Else switch direction
            if len(platform_hit_list) == 0:
                self.change_y = -6
            else:
                self.change_x *= -1


    def jump(self):
        """ Called when user hits 'jump' button. """

        # Check if on platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        #print(platform_hit_list)
        for item in platform_hit_list:
            if type(item) == SemiPlatform and self.change_y != 0:
                platform_hit_list.remove(item)
                #print("HI")
                #print(platform_hit_list)
                #print("")
        # If ok to jump, set our speed upwards
        if len(platform_hit_list) > 0:
            self.change_y = -8.7 #-8.6

    def changedirectionatedges(self):

        # Called if enemy and if enemy.falltype == no fall
        # Moves self down 2 and across width, then checks if colliding with blocks
        # If no, then change direction

        self.rect.y += 2
        if self.direction == "R":
            self.rect.x += self.width -3
        if self.direction == "L":
            self.rect.x -= self.width +3

        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        self.rect.y -= 2
        if self.direction == "R":
            self.rect.x -= self.width -3
        if self.direction == "L":
            self.rect.x += self.width +3

        if len(platform_hit_list) == 0:
            self.change_x *= -1


    # Player-controlled movement:
    def go_left(self):
        self.change_x = self.speed * -1

    def go_right(self):
        self.change_x= self.speed

    def stop(self):
        self.change_x = 0
'''
    def duck(self):
        self.height = 32
        self.image = pygame.Surface([self.width,self.height])

    def stand(self):
        self.height = 55
        self.image = pygame.Surface([self.width,self.height])
'''

        
class Player(Entity):
    def __init__(self):

        self.status = "player"

        self.lives = 3

        self.startx = 200
        self.starty = 384

        self.width = 32
        self.height = 64

        self.speed = 4.5 #4.5

        self.startvelocity = 0

        self.falltype = True

        self.graceon = False
        self.gracecount = 0

        super().__init__()


    def iscaught(self, lives, levelenemylist):
        if self.graceon == False:
            for enemy in levelenemylist:
                iscaught = pygame.sprite.spritecollide(self, levelenemylist, False)
                #for item in iscaught:
            for item in iscaught:
                # If item is a movingplatformenemy and player is moving up, do not lose a life
                if type(item) != MovingPlatformEnemy:   
                    self.lives -= 1
                    self.lifebar.skinchange()
                    self.grace()
                else:
                    if self.change_y >= 0:
                        self.lives -= 1
                        self.lifebar.skinchange()
                        self.grace()
        else:
            foo = 1


    def grace(self):
        self.graceon = True
        #self.image.fill(GRAY)

    def gracereload(self):
        if self.graceon == True:
            self.gracecount += 1
            if self.gracecount > 180:
                self.graceon = False
                self.gracecount = 0
                #self.image.fill(WHITE)

class Enemy(Entity):
    def __init__(self, x, y, width, height, falltype, color):
        self.status = "enemy"
        self.startx = x
        self.starty = y

        self.width = width
        self.height = height

        self.speed = 1

        self.color = color
        self.startvelocity = self.speed

        self.falltype = falltype

        super().__init__()

    def calcmove(self):
        if self.change_x > 0:
            self.go_right

        elif self.change_x < 0:
            self.go_left()


class MovingPlatformEnemy(Enemy):
    
    def __init__(self):

        #self.platform = platform
        self.image = None
        self.image = pygame.Surface([32,1])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()

        pygame.sprite.Sprite.__init__(self)  # Calls the sprite __init__()
        # Place at platform
        #self.rect.x = self.platform.rect.x +1
        #self.rect.y = self.platform.rect.y -1

    def update(self):
        self.rect.x = self.platform.rect.x#+2
        self.rect.y = self.platform.rect.y-1



        
class LifeBar(pygame.sprite.Sprite):
    def __init__(self):
        self.image = lifebar1
        #self.screen = screen
        #self.update

    def skinchange(self):
        if self.image == lifebar1:
            self.image = lifebar2
        elif self.image == lifebar2:
            self.image = lifebar3
        elif self.image == lifebar3:
            self.image = lifebar4

    def update(self,screen):
        screen.blit(self.image, [16,16])
'''
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        self.image = cursor
        pygame.mouse.set_visible(False)
        self.mousemoved = 0
        self.juststarted = True

    def update(self):
        self.pos = pygame.mouse.get_pos()
        # Check if mouse has moved
        if self.juststarted == False:
            if self.pos[0] == self.posx and self.pos[1] == self.posy:
                self.mousemoved += 1

            else:
                self.mousemoved == 0
        else:
            self.juststarted = False
        self.posx = self.pos[0]
        self.posy = self.pos[1]

    def draw(self, screen):
        #print(self.posx, self.posy)
        if self.posx < 0 or self.posx > SCREEN_WIDTH or self.posy < 0 or self.posy > SCREEN_HEIGHT:
            print("HI")
        else:
            if self.mousemoved < 120:
                screen.blit(self.image, [self.posx, self.posy])
'''


class Level(object):
    """ This is a generic super-class used to define a level.
        Creact a child class for each level with level-specific info """

    platform_list = None
    moving_platform_list = None
    still_platform_list = None
    enemy_list = None

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
             collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.moving_platform_list = pygame.sprite.Group()
        self.still_platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        self.lifebar = LifeBar()
        self.lifebar.player = self.player
        player.lifebar = self.lifebar


        self.background = None

    def update(self):
        #try:
        #    print(self.player.direction)
        #except:
        #    foo = 1

        self.platform_list.update()
        #self.enemy_list.update() # doesnt currently do anything, just speed them up
        self.player.iscaught(self.player.lives, self.enemy_list)
        self.player.gracereload()


    def draw(self, screen):
        screen.fill(BLUE) # <--- Change background here
        self.platform_list.draw(screen)
        #self.enemy_list.draw(screen)


class Level1(Level):

    def __init__(self, player):

        Level.__init__(self, player)

        platforms = []


        # Map Editor Key
        # P = Platform
        # S = Semi-Solid Platform
        # E = Enemy which can't fall down
        # A = Enemy which can fall down
        # 1 = Start of moving platform
        # 2 = End of moving platform
        # 3 = Start of spiked platform
        # 4 = End of spiked platform


        # 40 x 20 blocks (800 blocks total)

        level = [
            "                                        ", #1
            "                                        ", #2
            "            PPP                         ", #3
            "P                     1      2 PP       ", #4
            "PPPP             AP      PPP           P", #5
            "PP1    2         PPPP              A  PP", #6
            "          S E               SSS     PPPPP", #7
            "           SSSS       P                 ", #8
            "                      P  E              ", #9
            "                3   4    PPPPPPPP       ", #10
            "                PPPPP       PPP         ", #11
            "PPP                                    E", #12
            "        PPP                         PPPP", #13
            "      PPPPPPP                          P", #14
            "          PPPP     PPP        PPPP      ", #15
            "P                     P                 ", #16
            "PPP            PPP       P          PPPP", #17
            "PPPP        PPPPPPP     PPP       PPPPPP", #18
            "PPPPPPP   PPPPPPPPPPPPPPPPPP   PPPPPPPPP", #19
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", #20
            ]



        self.x = 0
        self.xa = 0
        self.y = 0
        self.ya = 0
        i = 1
        for row in level:
            for col in row:
                if col == "P":
                    if level[self.ya - 1][self.xa] == "P":
                        skin = random.choice([ground2, ground3])
                        p = SolidPlatform(self.x, self.y, skin)
                    else:
                        p = SolidPlatform(self.x, self.y, ground1)

                    p.player = self.player
                    self.still_platform_list.add(p)

                # Create Semiplatforms
                if col == "S":
                    s = SemiPlatform(self.x, self.y, semisolid)

                    s.player = self.player
                    self.still_platform_list.add(s)
                # Create moving platforms
                if col == "1" or col == "3":
                    skin = wood if col == "1" else spike
                    q = MovingPlatform(self.x, self.y, skin)
                    q.boundary_left = self.x+1# - 15# - 32
                    q.change_x = 1
                    q.player = self.player
                    q.level = self
                    self.moving_platform_list.add(q)
                    #self.platform_list.add(q)
                    if col == "3":
                        # Create enemy to go with moving platform
                        r = MovingPlatformEnemy()
                        r.platform = q
                        self.enemy_list.add(r)
                        r.level = self


                if col == "2" or col == "4":
                    q.boundary_right = self.x +31# + 15# + 32

                self.x += 32
                self.xa += 1
            self.y += 32
            self.ya += 1
            self.x = 0
            self.xa = 0

        # Create blocks just off-screen
        self.x = -32
        self.y = -128
        for i in range(2):
            for i in range(24):
                p = SolidPlatform(self.x, self.y, ground2)
                p.player = self.player
                self.still_platform_list.add(p)
                self.y += 32
            self.x = 1280
            self.y = 0


        #Loop for enemy placement

        self.x = 0
        self.y = 0
        for row in level:
            for col in row:
                if col == "E" or col == "A":
                    if col == "E":
                        e = Enemy(self.x, self.y, 32, 32, False, ORANGE)
                    elif col == "A":
                        e = Enemy(self.x, self.y, 32, 32, True, YELLOW)

                    self.enemy_list.add(e)
                    e.level = self

                self.x += 32
            self.y += 32
            self.x = 0

        # Create moving block
        #block = MovingPlatform(70,40, ground1)
        #block.rect.x = 1100
        #block.rect.y = 288
        #block.boundary_left = 1100
        #block.boundary_right = 1200
        #block.change_x = 1
        #block.player = self.player
        #block.level = self
        #self.platform_list.add(block)

        # Add the still platforms to the end of the platform list so that they get called after the moving platforms
        self.platform_list.add(self.moving_platform_list)
        self.platform_list.add(self.still_platform_list)
        #self.platform_list.add(self.moving_platform_list)


        '''
        # [xstart, ystart, width, height, color]
        enemies = [ [0,0,32, 32, ORANGE],
                  [400,200,32, 32, RED]
                  ]

        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4])
            self.enemy_list.add(enemy)
            enemy.level = self
       '''


class Game(object):
    ''' This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this class. '''

    def __init__(self):
        """ Constructor. Create all our attributes and initialize the game. """

        #self.cursor = Cursor()

        self.player = Player()

        self.level_list = []

        # Adds list of levels to the level list
        self.level = Level1(self.player)

        self.level_list.append(self.level)
        '''
        room = Room2()
        rooms.append(room)

        room = Room3()
        rooms.append(room)
        '''
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]

        self.active_sprite_list = pygame.sprite.Group()

        self.active_sprite_list.add(self.player)
        self.active_sprite_list.add(self.current_level.enemy_list)

        self.player.level = self.current_level
        #self.current_level.enemy_list = self.current_level

        pygame.mixer.music.load('Assets/BornUnderground.ogg')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
        pygame.mixer.music.play()

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_RETURN:
                    self.__init__()

                elif event.key == pygame.K_LEFT:
                    print("HI")
                    self.player.go_left()

                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()

                elif event.key == pygame.K_UP:
                    self.player.jump()
                #elif event.key == pygame.K_DOWN:
                    #self.player.duck()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                elif event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                #elif event.key == pygame.K_DOWN:
                    #self.player.stand()
            elif event.type == pygame.constants.USEREVENT:
                # This event is triggered when the song stops playing.
                pygame.mixer.music.play()
        return False


    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """

        self.current_level.update()

        self.active_sprite_list.update()

        #self.cursor.update()



        #if self.player.rect.right > SCREEN_WIDTH:
        #    self.player.rect.right = SCREEN_WIDTH

        #if self.player.rect.left < 0:
        #    self.player.rect.left = 0



    def display_frame(self, screen):
        self.current_level.draw(screen)
        self.current_level.lifebar.update(screen)
        self.active_sprite_list.draw(screen)
        #self.cursor.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()



def main():

    pygame.init()

    # Set the width and the height of the screen [width, height]
    global size
    size = (SCREEN_WIDTH,SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    fontGO = pygame.font.SysFont('Calibri', 150, True, False)

    pygame.display.set_caption("Dwarf Game")

    #background = background.convert()

    #background.fill(black)

    # Load images
    global ground1
    ground1 = pygame.image.load("Assets/Ground1.PNG").convert()

    global ground2
    ground2 = pygame.image.load("Assets/Ground2.PNG").convert()

    global ground3
    ground3 = pygame.image.load("Assets/Ground3.PNG").convert()

    global dwarfR
    dwarfR = pygame.image.load("Assets/Dwarf.PNG").convert()

    global dwarfL
    dwarfL = pygame.transform.flip(dwarfR, True, False)

    global enemy1R
    enemy1R = pygame.image.load("Assets/Enemy1.PNG").convert()

    global enemy1L
    enemy1L = pygame.transform.flip(enemy1R, True, False)

    global lifebar1
    lifebar1 = pygame.image.load("Assets/LifeBar1.PNG").convert()

    global lifebar2
    lifebar2 = pygame.image.load("Assets/LifeBar2.PNG").convert()

    global lifebar3
    lifebar3= pygame.image.load("Assets/LifeBar3.PNG").convert()

    global lifebar4
    lifebar4 = pygame.image.load("Assets/LifeBar4.PNG").convert()

    global wood
    wood = pygame.image.load("Assets/Wood.PNG")

    global spike
    spike = pygame.image.load("Assets/Spike.PNG")

    global semisolid
    semisolid = pygame.image.load("Assets/SemiSolid.PNG")




    #global cursor
    #cursor = pygame.image.load("dwarven_gauntlet.PNG")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()


    done = False

    # ------- Main Program Loop -------
    while not done:

        # --- Main event loop

        # Update object positions, check for sollisions
        game.run_logic()

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Draw the current frame
        game.display_frame(screen)

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit
    pygame.quit()
