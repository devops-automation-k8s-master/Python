import pygame
import time
import random
#intiate pygame functions
pygame.init()
dWidth=800
dHeight=600

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)


def things(x,y,w,h,color):
    pygame.draw.rect(gameDisplay,color,[x,y,w,h])
carImg=pygame.image.load("sp.png")
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
gameDisplay = pygame.display.set_mode((dWidth,dHeight))
pygame.display.set_caption("A bit Racey")
clock = pygame.time.Clock()

def text_objects(text,font):
    textSurf=font.render(text,True,black)
    return textSurf, textSurf.get_rect()


def messageDisplay(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    textSurf, textRect=text_objects(text,largeText)
    textRect.center=((dWidth/2),(dHeight/2))
    gameDisplay.blit(textSurf,textRect)
    pygame.display.update()
    time.sleep(2)
    gameloop()





def crash():
    messageDisplay("You Crashed")

def gameloop():
    x=(dWidth*.45)
    y=(dHeight*.8)
    x_change=0
    startx=random.randrange(0,dWidth)
    starty=0
    tspeed=20
    tw=100
    th=100

    gameExit =False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit=True
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change=-5
                if event.key == pygame.K_RIGHT:
                    x_change=5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change=0

            print(event)
        x +=x_change
        gameDisplay.fill(white)
        things(startx,starty,tw,th,black)
        starty+=tspeed
        car(x,y)

        if x>dWidth-50 or x<0:
            crash()
        #def things(x,y,w,h,color):
        if starty > dHeight:
            starty=0-tw
            startx=random.randrange(0,dWidth)
        if y<starty+th:
            print("collision of y")
            if x<= startx and startx <= x+50 or x<= startx+tw and startx < x+50:
                crash()
        pygame.display.update()
        clock.tick(60)

gameloop()
pygame.quit()
quit()
