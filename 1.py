import pygame
pygame.init()

# This goes outside the while loop, near the top of the program
walkRight = [pygame.image.load('images\R1.png'), pygame.image.load('images\R2.png'), pygame.image.load('images\R3.png'), pygame.image.load('images\R4.png'), pygame.image.load('images\R5.png'), pygame.image.load('images\R6.png'), pygame.image.load('images\R7.png'), pygame.image.load('images\R8.png'), pygame.image.load('images\R9.png')]
walkLeft = [pygame.image.load('images\L1.png'), pygame.image.load('images\L2.png'), pygame.image.load('images\L3.png'), pygame.image.load('images\L4.png'), pygame.image.load('images\L5.png'), pygame.image.load('images\L6.png'), pygame.image.load('images\L7.png'), pygame.image.load('images\L8.png'), pygame.image.load('images\L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('images\standing.png')

screen=(500,480)
win = pygame.display.set_mode(screen)

pygame.display.set_caption("my first game!!")

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound("hit.wav")
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

score=0

seebox=-1

class player(object):
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing = True
        self.reloadTime=10
        self.hitbox=(self.x+15,self.y+15,33,50)

    def draw(self,win):
        if not self.standing:
            if self.walkCount +1 >= 27:
                self.walkCount=0
            if self.left:
                win.blit(walkLeft[int(self.walkCount//3)],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[int(self.walkCount//3)],(self.x,self.y))
                self.walkCount+=1
        else:
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            elif self.left:
                win.blit(walkLeft[0],(self.x,self.y))
            else:
                win.blit(char,(self.x,self.y))
                
        self.hitbox=(self.x+15,self.y+15,33,50)
        pygame.draw.rect(win, (255,0,0),self.hitbox,seebox)

    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        self.isJump = False
        self.jumpCount=10
        self.standing = True
        self.right = False
        self.left = False
        font1 = pygame.font.SysFont("comicsans",100)
        text = font1.render("-20",1,(255,0,0))
        win.blit(text,((screen[0]/2)-(text.get_width()/2),(screen[1]/2)-(text.get_height()/2)))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   i=301
                   pygame.quit()
                   
class proyectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class enemy(object):

    walkRight = [pygame.image.load('images\R1E.png'), pygame.image.load('images\R2E.png'), pygame.image.load('images\R3E.png'), pygame.image.load('images\R4E.png'), pygame.image.load('images\R5E.png'), pygame.image.load('images\R6E.png'), pygame.image.load('images\R7E.png'), pygame.image.load('images\R8E.png'), pygame.image.load('images\R9E.png'),pygame.image.load('images\R10E.png'),pygame.image.load('images\R11E.png')]
    walkLeft = [pygame.image.load('images\L1E.png'), pygame.image.load('images\L2E.png'), pygame.image.load('images\L3E.png'), pygame.image.load('images\L4E.png'), pygame.image.load('images\L5E.png'), pygame.image.load('images\L6E.png'), pygame.image.load('images\L7E.png'), pygame.image.load('images\L8E.png'), pygame.image.load('images\L9E.png'),pygame.image.load('images\L10E.png'),pygame.image.load('images\L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.wigth=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.walkCount=0
        self.vel=3
        self.hitbox=(self.x+17,self.y+2,31,57)
        self.completeHealth=100
        self.health=self.completeHealth
        self.visible=True

    def draw(self,win):
        self.move()
        
        if self.visible: 
            if self.walkCount +1 >= 33:
                self.walkCount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1

            pygame.draw.rect(win,(255,0,0),(self.hitbox[0]-15,self.hitbox[1]-5,50,5))
            pygame.draw.rect(win,(0,128,0),(self.hitbox[0]-15,self.hitbox[1]-5,50*(self.health/self.completeHealth),5))
            self.hitbox=(self.x+20,self.y,28,60)
            pygame.draw.rect(win,(255,0,0),self.hitbox,seebox)
        
          
    def move(self):
        if self.vel>0:
            if self.x + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel * -1
                self.walkCount=0
        else:
            if self.x + self.vel > self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel * -1
                self.walkCount=0
        
    def hit(self):
        if self.health>0:
            pass
        else:
            self.visible=False
            
        print("hit")
        
        
        
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render("Score: "+ str(score), 1, (0,0,0))
    win.blit(text,(350,10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update() 


#MAIN LOOP


font = pygame.font.SysFont("comicsans",30,True,True)
man=player(300,410,64,64)
goblin=enemy(100,410,64,64,400)
run=True
bullets=[]

while run:
    clock.tick(27)


    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2 ]> goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                score-=20
                man.hit()

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    
    for bullet in bullets:
        if goblin.visible:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hitSound.play()
                    score+=10
                    goblin.health-=10
                    goblin.hit()
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))            

    keys=pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        bulletSound.play()
        if man.left:
            facing=-1
        else:
            facing=1
            
        if len(bullets) < 5 and man.reloadTime >= 5:
            bullets.append(proyectile(round(man.x + man.width//2),round(man.y+man.height//2),6,(0,0,0),facing))
            man.reloadTime=0
            
    man.reloadTime+=1
    
    if keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.left=True
        man.right=False
        man.standing=False
        
        
    elif keys[pygame.K_d] and man.x < screen[0]-man.width:
        man.x += man.vel
        man.left=False
        man.right=True
        man.standing=False
    else:
        man.standing=True
        
    if not man.isJump:
        if keys[pygame.K_w]:
            man.isJump = True
    else:
        if man.jumpCount >= 0 and man.jumpCount <= 10:
            man.y -= (man.jumpCount**2)*0.5
            man.jumpCount-=1
        elif man.jumpCount < 0 and man.jumpCount >= -10: 
            man.y += (man.jumpCount**2)*0.5
            man.jumpCount-=1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()


    
pygame.quit()
