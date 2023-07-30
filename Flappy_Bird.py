#Modules
import pygame
pygame.init()
import time
import threading
import random

#Variables
Clock = pygame.time.Clock()
FPS = 240
x = 300
y = 300
Height = 600
Width = 600
BirdHeight = 60
BirdWidth = BirdHeight/1.4367816092
Screen = pygame.display.set_mode((Height, Width))
FlappyBird = pygame.image.load("Vader_Bird.png")
FlappyBird = pygame.transform.scale(FlappyBird, (BirdHeight, BirdWidth)).convert_alpha()
FlappyBackground = pygame.image.load("Flappy_Background.png")
FlappyBackground = pygame.transform.scale(FlappyBackground, (Height, Width))
PlayButton = pygame.image.load("PlayButton.png")
PlayButton = pygame.transform.scale(PlayButton,(300,300))
Screen.fill((80,0,150))
pygame.display.set_caption("Flappy Bird")
PlayButtonRect = pygame.Rect(192,273,237,56)
PlayButtonRect = pygame.draw.rect(Screen, (0,0,0), PlayButtonRect)

#Lambda for resetting screen
ResetScreen = lambda x,y: Screen.blit(FlappyBackground, (x,y))
ResetScreen(0,0)
Screen.blit(PlayButton, (150,150))
FinishedJumping = False
MovingDown = False
PipesList = []
Running = True


#Classes

#Bird Class for Character

class Bird:
    #Initialisation function
    def __init__(self,posX, posY, sizeX, sizeY, image, gravity, JumpPower, JumpTime):
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.image = image
        self.velY = 0
        self.velX = 0
        self.gravity = gravity
        self.JumpPower = JumpPower
        self.JumpTime = JumpTime
        self.RectObject = pygame.Rect(self.posX+(0.18*BirdWidth), self.posY+(0.05*BirdHeight), BirdHeight/1.2, BirdHeight/1.7)
    #Main Jump Method
    def Jump(self):
        #self.posY -= self.JumpPower
        InitialEpochTime = time.time()
        DividingLambda = lambda x,y:x/y
        MidTime = DividingLambda(self.JumpTime, 2)
        TickTime = 240
        while (time.time() - InitialEpochTime) <= self.JumpTime:
            if (time.time() - InitialEpochTime) < MidTime:
                self.posY -= self.JumpPower/(self.JumpTime*TickTime)
            else:
                self.posY -= self.JumpPower/(self.JumpTime*TickTime)

            Clock.tick(TickTime)
    #Draw Character Method
    def Draw(self, window):
        self.RectObject = pygame.Rect(self.posX+(0.18*BirdWidth), self.posY+(0.05*BirdHeight), BirdHeight/1.2, BirdHeight/1.7)
        pygame.draw.rect(Screen, (1,1,1,0), self.RectObject)
        ResetScreen(0,0)
        window.blit(self.image, (self.posX,self.posY))

#Pipe Class
class Pipe:
    def __init__(self,width, height, color, LeftSpace, StartPoint):
        self.Width = width
        self.color = color
        self.Height = height
        self.LeftSpace = LeftSpace
        self.StartPoint = StartPoint
        self.FirstPipeLength = random.randint(50,300)
        self.SecondPipeLength = 600 - self.LeftSpace - self.FirstPipeLength
        self.ProgressionNumber = 0
        self.FirstRect = pygame.Rect(self.StartPoint,0, self.Width, self.FirstPipeLength)
        self.SecondRect = pygame.Rect(self.StartPoint, 600 - self.SecondPipeLength, self.Width, self.SecondPipeLength)
    
    def InitializePipes(self):
        pygame.draw.rect(Screen, self.color, self.FirstRect)
        pygame.draw.rect(Screen, self.color, self.SecondRect)
    
    def UpdatePipes(self):
        self.ProgressionNumber += 1.5
        FirstPipe = pygame.Rect(self.StartPoint - self.ProgressionNumber,0, self.Width, self.FirstPipeLength)
        SecondPipe = pygame.Rect(self.StartPoint - self.ProgressionNumber, 600-self.SecondPipeLength, self.Width, self.SecondPipeLength)
        self.FirstRect = FirstPipe
        self.SecondRect = SecondPipe
        pygame.draw.rect(Screen, self.color, self.FirstRect)
        pygame.draw.rect(Screen, self.color, self.SecondRect)
        


#Producing Pipe Function
def ProducePipe():
    time.sleep(0.5)
    while Running:
        Pipes = Pipe(10, 10, (random.randint(1,255),random.randint(1,255),random.randint(1,255)), random.randint(150,200), 500)
        PipesList.append(Pipes)
        time.sleep(1)

def RemovePipe():
    time.sleep(2.5)
    while Running:
        time.sleep(1)
        PipesList.pop(0)
    







#Main Function
def main():
    InMenu = True
    running = True
    MovingDown = False
    #Initializing Bird
    Gravity = 1
    GravityIncrease = 0.04
    ConstGravityIncrease = 0.04
    VaderBird = Bird(220,300, BirdHeight, BirdWidth, FlappyBird, Gravity, 50, 0.05)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and InMenu:
                mousepos = pygame.mouse.get_pos()
                ClickedPlay = PlayButtonRect.collidepoint(mousepos)
                if ClickedPlay:
                    InMenu = False
                    VaderBird.Draw(Screen)
                    MovingDown = True
                    PipeProduction = threading.Thread(target=ProducePipe)
                    PipeProduction.start()
                    PipeRemoval = threading.Thread(target=RemovePipe)
                    PipeRemoval.start()
            if event.type == pygame.KEYDOWN and not InMenu and MovingDown:
                if event.key == pygame.K_SPACE:
                    VaderBird.gravity = Gravity
                    GravityIncrease = ConstGravityIncrease
                    JumpThread = threading.Thread(target=VaderBird.Jump)
                    JumpThread.start()
                    MovingDown = False
        if MovingDown:
            VaderBird.Draw(Screen)
            VaderBird.posY += VaderBird.gravity
            VaderBird.gravity += GravityIncrease
            GravityIncrease += 0.001
        elif not InMenu:
            if not JumpThread.is_alive():
                MovingDown = True
            VaderBird.Draw(Screen)
        if not InMenu:
            for Pipe in PipesList:
                Pipe.UpdatePipes()
        try:
            Collision1 = pygame.Rect.colliderect(VaderBird.RectObject, PipesList[len(PipesList)-2].FirstRect)
            Collision2 = pygame.Rect.colliderect(VaderBird.RectObject, PipesList[len(PipesList)-2].SecondRect)
            if Collision1 or Collision2:
                running = False
        except IndexError:
            pass
        if VaderBird.posY > 600 or VaderBird.posY < 0:
            running = False
        pygame.display.flip()
        Clock.tick(120)


#Calling main function
main()
Running = False
