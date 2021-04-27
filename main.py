import pygame
import math


pygame.mixer.init()
pygame.init()


windowwidth = 800
windowheight = 600
#win = pygame.display.set_mode((windowwidth,windowheight))
win = pygame.display.set_mode((windowwidth,windowheight))
pygame.display.set_caption("Sharp Shooter")
clock = pygame.time.Clock()

#Declare fonts
gamefont = pygame.font.SysFont('Copperplate', 50)
reloadfont = pygame.font.SysFont('Copperplate', 13)
titlefont = pygame.font.SysFont('Copperplate', 100)

#Load images in
mainbg = pygame.image.load('hillbackground.jpg')
flyright = [pygame.image.load('birds-flyright/bird1.png'), pygame.image.load('birds-flyright/bird2.png'), pygame.image.load('birds-flyright/bird3.png')]
walkright = [pygame.image.load('birds-walkright/bird1.png'), pygame.image.load('birds-walkright/bird2.png'), pygame.image.load('birds-walkright/bird3.png'), pygame.image.load('birds-walkright/bird4.png'), pygame.image.load('birds-walkright/bird5.png'), pygame.image.load('birds-walkright/bird6.png')]
walkleft = [pygame.image.load('birds-walkleft/bird1.png'), pygame.image.load('birds-walkleft/bird2.png'), pygame.image.load('birds-walkleft/bird3.png'), pygame.image.load('birds-walkleft/bird4.png'), pygame.image.load('birds-walkleft/bird5.png'), pygame.image.load('birds-walkleft/bird6.png')]
bulletimg = pygame.image.load('bullet.png')
bulletimg2 = pygame.image.load('bullet2.png')



#Load sounds in
shotgunshot = pygame.mixer.Sound('shotgun-shot.mp3')
shotgunreload = pygame.mixer.Sound('shotgun-reload.mp3')
shotgunrefill = pygame.mixer.Sound('shotgun-refill.mp3')
hoversound =  pygame.mixer.Sound('hoversound.wav')
selectsound =  pygame.mixer.Sound('selectsound.wav')
pointsound =  pygame.mixer.Sound('pointsound.wav')

#Set framerate
framerate = 60  
#Set color of start and quit buttons
startcolor = (0,0,0)
quitcolor = (0,0,0)

class shooter():
    def __init__(self):
        self.score = 0
        #Keeps count of which sprite is being blitted to screen
        self.spritecount = 0
        self.bullets = 5

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
        #Must include self.shootflag == False to ensure the gunshot sound only play once
        if event.type == pygame.MOUSEBUTTONDOWN and self.shootflag == False and player.bullets > 0:
            self.shootflag = True
            #Can put below code in move() if you want bullet to follow arrow (Could include it in a sniper type gun)
            self.mousepos = pygame.mouse.get_pos()
            pygame.mixer.Sound.play(shotgunshot)
            pygame.mixer.Sound.play(shotgunreload)
            player.bullets -= 1
           

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

    def __init__(self, x, y, vel, width, height, pathstart, pathend, sprites):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        self.hit = False
        self.spritecount = 0
        self.pathstart = pathstart
        self.pathend = pathend
        self.sprites = sprites
        self.hitbox = (self.x, self.y, self.width + 10, self.height)

    def move(self):

        #Reset bird if been hit
        if self.hit == True:
            self.x = 0
            self.hit = False

        if self.x < self.pathend:
            self.x += self.vel
            
        else: 
            self.x = self.pathstart

        #ALways add 10 width to get hitbox to fit
        self.hitbox = (self.x, self.y, self.width + 10, self.height)

    def draw(self):
        
        win.blit(self.sprites[math.trunc(self.spritecount)], (self.x, self.y))
        #Increase the spritecount so the sprite only changes the suitable number of times for the framerate (Use // not / so if you adding e.g 0.1 everytime no errors occur)
        if self.spritecount < len(self.sprites) - (len(self.sprites)/(framerate)):  
            self.spritecount += len(self.sprites)/(framerate)
        else:
            self.spritecount = 1

    def checkhit(self):

        for i in range(self.hitbox[2] + 1):
            if ((bullet.hitbox[0] + i >= self.hitbox[0]) and (bullet.hitbox[0] + i <= self.hitbox[0] + self.hitbox[2])) and ((bullet.hitbox[1] + i >= self.hitbox[1]) and (bullet.hitbox[1] + i <= self.hitbox[1] + self.hitbox[3])):
                if self.hit == False:
                    player.score += 100
                    self.hit = True    
                    pygame.mixer.Sound.play(pointsound)


class walkingbird():

    def __init__(self, x, y, vel, width, height, pathstart, pathend):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height
        self.spritecount = 0
        self.pathstart = pathstart
        self.pathend = pathend
        self.reverse = False

    def draw(self):

        if self.reverse == False:
        
            win.blit(walkright[math.trunc(self.spritecount)], (self.x, self.y))
            if self.spritecount < len(walkright) - (len(walkright)/(framerate)):  
                self.spritecount += len(walkright)/(framerate)
            else:
                self.spritecount = 1
        else:
            
            win.blit(walkleft[math.trunc(self.spritecount)], (self.x, self.y))
            if self.spritecount < len(walkleft) - (len(walkleft)/(framerate)):  
                self.spritecount += len(walkleft)/(framerate)
            else:
                self.spritecount = 1

    def move(self):
        #Always put move before draw
        #Reset bird if been hit
        if self.x < self.pathend and self.reverse == False:
            self.x += self.vel
            
        else: 
            self.reverse = True

        #Reverse if reached end
        if self.reverse and self.x > self.pathstart:
            self.x -= self.vel
        else:
            self.reverse = False

        




#Instantiate objects
player = shooter()
bullet = missile(10, 5, 10)
pigeon = bird(0, 100, 5, 50, 50, 0, windowwidth, flyright)
pigeonwalk = walkingbird(247, 370, 0.5, 20, 20, 247, 537)

def drawgamewindow():
    win.blit(mainbg, (0,0))
    #Draw in score
    scoresurfaceinner = gamefont.render("Score: " + str(player.score), True, (255,215,0))
    win.blit(scoresurfaceinner,(10,10))
    scoresurfaceouter = gamefont.render("Score: " + str(player.score), True, (0,0,0))
    win.blit(scoresurfaceouter,(8,8))
    #Draw in bullets left
    for i in range(player.bullets):
        win.blit(bulletimg2, (350 + (i*20), 25))

    #Draw in reload button if bullets empty
    if player.bullets == 0:
        pygame.draw.circle(win, (255,215,0), (703, 503), 30)
        pygame.draw.circle(win, (0,0,0), (700, 500), 30)
        reloadsurfaceinner = reloadfont.render("RELOAD", True, (255,255,255))
        win.blit(reloadsurfaceinner, (674, 492))
        mousepos = pygame.mouse.get_pos()
        #Change color of startbutton when hovering
        if (mousepos[0] >= 670 and mousepos[0] <= 730) and (mousepos[1] >= 470 and mousepos[1] <= 530):
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(shotgunrefill)
                player.bullets = 5
    
    pigeon.draw()
    bullet.draw()
    pygame.display.update()

def drawstartwindow():
    win.blit(mainbg, (0,0))
    startsurface = gamefont.render("Start", True, startcolor)
    quitsurface = gamefont.render("Quit", True, quitcolor)
    win.blit(startsurface, (20,10))
    win.blit(quitsurface, (20,50))
    pigeonwalk.draw()
    #Draw title
    titlesurfaceinner = titlefont.render("Pigeon Frenzy", True, (255,215,0), )
    win.blit(titlesurfaceinner, (30, windowheight//2 - 100))
    #Outline
    titlesurfaceouter = titlefont.render("Pigeon Frenzy", True, (0,0,0))
    win.blit(titlesurfaceouter, (28, windowheight//2 - 102))
    pygame.display.update()

def playstartmusic():
    #Load music in
    pygame.mixer.music.load("startwindowmusic.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
playstartmusic()

def playgamemusic():
    global gamemusicflag
    #Makes sure game music not restarted each loop
    if gamemusicflag == False:
        #Load music in
        pygame.mixer.music.load("gamemusic.mp3")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        gamemusicflag = True

# pygame.mouse.set_visible(False) #/// Use for when we have the gun in the game, to remove mouse
run = True
startwindow = True
gamemusicflag = False
hoverplayflag1 = False
hoverplayflag2 = False
#MAINLOOP
while run:
    clock.tick(framerate)

    while startwindow and run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pigeonwalk.move()
        drawstartwindow()
        mousepos = pygame.mouse.get_pos()
        #Change color of startbutton when hovering
        if (mousepos[0] >= 20 and mousepos[0] <= 160) and (mousepos[1] >= 10 and mousepos[1] <= 50):
            startcolor = (0,200,0)
            #To ensure hoverplay only played once
            
            if hoverplayflag1 == False:
                
                pygame.mixer.Sound.play(hoversound)
                hoverplayflag1 = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                startwindow = False
                pygame.mixer.Sound.play(selectsound)
                pygame.mixer.music.pause()
                pygame.time.delay(500)
                
        else:
            startcolor = (0, 0, 0)
            hoverplayflag1 = False

        if (mousepos[0] >= 20 and mousepos[0] <= 140) and (mousepos[1] >= 55 and mousepos[1] <= 95):
            quitcolor = (200,0,0)

            if hoverplayflag2 == False:
                pygame.mixer.Sound.play(hoversound)
                hoverplayflag2 = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pygame.quit()
        else:
            
            quitcolor = (0, 0, 0)
            hoverplayflag2 = False

    #Must be after start window so bullet doesnt shoot when pressing start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
   
    playgamemusic()
    bullet.shoot()
    bullet.move()
    pigeon.move()
    pigeon.checkhit()
    drawgamewindow()
