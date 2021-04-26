import pygame
pygame.init()

windowwidth = 500
windowheight = 500
win = pygame.display.set_mode((windowwidth, windowheight))

pygame.display.set_caption("Sharp Shooter")
clock = pygame.time.Clock()

#Load images in
mainbg = pygame.image.load('hillsbackground.jpg')


class shooter():
    def __init__(self):
        self.score = 0

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
    
    def draw(self):
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height))

    def shoot(self):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.shootflag = True
            
#To get to move diagonally, have different velocities for x and y (Use graph eqn's to help, y=mx+c based on the angle you shooting at)
    #Always called with shoot()
    def move(self):
        
        if self.shootflag == True and self.y > 0:
            #Get mouse pos
            self.mousepos = pygame.mouse.get_pos()

            #Calculate gradient from shooter to mouse (Use y=mx + c)
            self.gradient = (windowheight - self.mousepos[1])/((windowwidth/2) - self.mousepos[0])
       
            #Calculate y intercept
            self.yintercept = self.mousepos[1] - (self.gradient*self.mousepos[0])
            
            self.y -= self.vel
            print("y: ", self.y)

            #Calculate new x-value
            self.x  = ((self.y - self.yintercept)/self.gradient)
            print("x: ", self.x)
           
        
            
        
        else: 
            self.y = self.yorigin
            self.x = self.xorigin
            self.shootflag = False

        
class bird():

    def __init__(self, vel, width, height):
        self.x = -10
        self.y = -10
        self.vel = vel
        self.width = width
        self.width = height

#Instantiate objects
player = shooter()
bullet = missile(10, 5, 10)
pigeon = bird(5, 50, 50)

def drawgamewindow():
    win.blit(mainbg, (0,0))
    bullet.draw()
    pygame.display.update()

#pygame.mouse.set_visible(False) /// Use for when we have the gun in the game, to remove mouse
run = True
#MAINLOOP
while run:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    
    bullet.shoot()
    bullet.move()
    drawgamewindow()