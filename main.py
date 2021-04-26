import pygame
import math


pygame.init()


windowwidth = 800
windowheight = 600
#win = pygame.display.set_mode((windowwidth,windowheight))
win = pygame.display.set_mode((windowwidth,windowheight))
pygame.display.set_caption("Sharp Shooter")
clock = pygame.time.Clock()
gamefont = pygame.font.SysFont('Comic Sans', 50)

#Load images in
mainbg = pygame.image.load('hillbackground.jpg')
flyright = [pygame.image.load('birds/bird1.png'), pygame.image.load('birds/bird2.png'), pygame.image.load('birds/bird3.png')]
bulletimg = pygame.image.load('bullet.png')

#Set framerate
framerate = 60

class shooter():
    def __init__(self):
        self.score = 0
        #Keeps count of which sprite is being blitted to screen
        self.spritecount = 0

class missile():
    
    def __init__(self, vel, width, height):
        self.gradient = 0
        self.xorigin = windowwidth//2
        self.yorigin = windowheight
        self.x = self.xorigin
        self.y = self.yorigin
        self.yintercept = 0
        self.vel = vel
        self.width = width
        self.height = height
        self.shootflag = False
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self):
        
        win.blit(bulletimg, (self.x, self.y))

    def shoot(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shootflag = True
            #Can put below code in move() if you want bullet to follow arrow (Could include it in a sniper type gun)
            self.mousepos = pygame.mouse.get_pos()

#To get to move diagonally, have different velocities for x and y (Use graph eqn's to help, y=mx+c based on the angle you shooting at)
    #Always called with shoot()

    def move(self):
        
        if self.shootflag == True and self.y > 0:
            #Get mouse pos
            

            try:
                #Calculate gradient from shooter to mouse (Use y=mx + c)
                self.gradient = (windowheight - self.mousepos[1])/((windowwidth/2) - self.mousepos[0])
            
                #Calculate y intercept
                self.yintercept = self.mousepos[1] - (self.gradient*self.mousepos[0])
                self.y -= self.vel

                #Calculate new x-value
                self.x  = ((self.y - self.yintercept)/self.gradient)  

            except ZeroDivisionError:
                pass 
            
        else: 
            self.y = self.yorigin
            self.x = self.xorigin
            self.shootflag = False

        #Make sure to update hitbox whenever x and y are updated (Usually at end of move)
        self.hitbox = (self.x, self.y, self.width, self.height)
class bird():

    def __init__(self, vel, width, height):
        self.x = 0
        self.y = 100
        self.vel = vel
        self.width = width
        self.height = height
        self.hit = False
        self.spritecount = 0
        self.hitbox = (self.x, self.y, self.width + 10, self.height)

    def move(self):

        #Reset bird if been hit
        if self.hit == True:
            self.x = 0
            self.hit = False

        if self.x < windowwidth:
            self.x += self.vel
            
        else: 
            self.x = 0

        #ALways add 10 width to get hitbox to fit
        self.hitbox = (self.x, self.y, self.width + 10, self.height)

    def draw(self):
        
        win.blit(flyright[math.trunc(self.spritecount)], (self.x, self.y))
        #Increase the spritecount so the sprite only changes the suitable number of times for the framerate (Use // not / so if you adding e.g 0.1 everytime no errors occur)
        if self.spritecount < len(flyright) - (len(flyright)/(framerate/2)):  
            self.spritecount += len(flyright)/(framerate//2)
        else:
            self.spritecount = 1

    def checkhit(self):

        for i in range(self.hitbox[2] + 1):
            if ((bullet.hitbox[0] + i >= self.hitbox[0]) and (bullet.hitbox[0] + i <= self.hitbox[0] + self.hitbox[2])) and ((bullet.hitbox[1] + i >= self.hitbox[1]) and (bullet.hitbox[1] + i <= self.hitbox[1] + self.hitbox[3])):
                if self.hit == False:
                    player.score += 100
                    self.hit = True          

#Instantiate objects
player = shooter()
bullet = missile(10, 5, 10)
pigeon = bird(5, 50, 50)

def drawgamewindow():
    win.blit(mainbg, (0,0))

    #Draw in score
    scoresurface = gamefont.render("Score: " + str(player.score), True, (0,0,0))
    win.blit(scoresurface,(10,10))
    pigeon.draw()
    bullet.draw()
    pygame.display.update()

# pygame.mouse.set_visible(False) #/// Use for when we have the gun in the game, to remove mouse
run = True
#MAINLOOP
while run:
    clock.tick(framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    
    bullet.shoot()
    bullet.move()
    pigeon.move()
    pigeon.checkhit()
    drawgamewindow()