#Modules
import pygame
pygame.init()
import time
import threading
import random

#Variables
Clock = pygame.time.Clock()
FPS = 240
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
PipeThickness = 30
OpenSpaceRangeForPipe = (150,200)
PipePerXSeconds = 1 
PipeSpeed = 1.5



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
        self.Jumping = False
    #Main Jump Method
    def Jump(self):
        if self.Jumping:
            return None
        self.Jumping = True
        InitialEpochTime = time.time()
        DividingLambda = lambda x,y:x/y
        MidTime = DividingLambda(self.JumpTime, 2)
        TickTime = 240
        Multiplier = 1
        while (time.time() - InitialEpochTime) <= self.JumpTime:
            if (time.time() - InitialEpochTime) < MidTime:
                self.posY -= self.JumpPower/(self.JumpTime*TickTime) * Multiplier
            else:
                self.posY -= self.JumpPower/(self.JumpTime*TickTime) * Multiplier
            Multiplier += 0.02
            Clock.tick(TickTime)
        self.Jumping = False
    #Draw Character Method
    def Draw(self, window):
        self.RectObject = pygame.Rect(self.posX+(0.18*BirdWidth), self.posY+(0.05*BirdHeight), BirdHeight/1.2, BirdHeight/1.7)
        pygame.draw.rect(Screen, (1,1,1,0), self.RectObject)
        ResetScreen(0,0)
        window.blit(self.image, (self.posX,self.posY))

#Pipe Class
class Pipe:
    def __init__(self,width, height, color, LeftSpace, StartPoint, Speed):
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
        self.PipeSpeed = Speed
    def InitializePipes(self):
        pygame.draw.rect(Screen, self.color, self.FirstRect)
        pygame.draw.rect(Screen, self.color, self.SecondRect)
    
    #Main Pipe Method
    def UpdatePipes(self):
        self.ProgressionNumber += self.PipeSpeed
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
        Pipes = Pipe(PipeThickness, PipeThickness, (random.randint(1,255),random.randint(1,255),random.randint(1,255)), random.randint(OpenSpaceRangeForPipe[0], OpenSpaceRangeForPipe[1]), 500, PipeSpeed)
        PipesList.append(Pipes)
        time.sleep(PipePerXSeconds)

#Removing Pipe Function
def RemovePipe():
    time.sleep(2.5)
    while Running:
        time.sleep(PipePerXSeconds)
        PipesList.pop(0)

#Accessory Function for collisions
def WhichIndex(delay):
    if delay > 1.4:
        return 1
    else:
        return 2
    

#Main Function
def main():
    InMenu = True
    running = True
    MovingDown = False
    #Initializing Bird
    Gravity = 1
    GravityIncrease = 0.04
    ConstGravityIncrease = 0.04
    VaderBird = Bird(220,300, BirdHeight, BirdWidth, FlappyBird, Gravity, 50, 0.125)
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
            Collision1 = pygame.Rect.colliderect(VaderBird.RectObject, PipesList[len(PipesList)-WhichIndex(PipePerXSeconds)].FirstRect)
            Collision2 = pygame.Rect.colliderect(VaderBird.RectObject, PipesList[len(PipesList)-WhichIndex(PipePerXSeconds)].SecondRect)
            if Collision1 or Collision2:
                running = False
        except IndexError:
            pass
        if VaderBird.posY > 600 or VaderBird.posY < 0:
            running = False
        pygame.display.update()
        Clock.tick(120)


#Calling main function
main()
Running = False
