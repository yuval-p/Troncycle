import random
import pygame
import math
import time
import threading
import tst
import vlc

pygame.init()

#settings
screenSize = [1280,768]
numOfTurns = 5
player1Color = [(0, 0, 255),(255, 0,0)]
player2Color = [(255, 0,0),(0, 0, 255)]
#sensorInput = tst.sensor_input()


background = 'BlackBackground.gif'
background_menu = 'tron-menus.jpg'


END_GAME = 1
QUIT = 2
NEW_GAME = 3

myfont = pygame.font.SysFont("monospace", 30)
maenuFont = pygame.font.SysFont("monospace", 70)

#screen = pygame.display.set_mode(screenSize)
screen = pygame.display.set_mode(screenSize,pygame.FULLSCREEN)

# TODO change to the sensors input..
def keyPress(sensor1,sensor2):


    
    if pygame.key.get_pressed()[pygame.K_LEFT]:
         sensor1.setAngle(-5)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
         sensor1.setAngle(5)
    if pygame.key.get_pressed()[pygame.K_UP]:
        sensor1.setSpeed(1)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        sensor1.setSpeed(-1)

#    sensor1.setAngle(sensorInput.getAngle1())
#    sensor1.setSpeed(sensorInput.getSpeed1())
#    print(sensorInput.getSpeed2())
#    print(sensorInput.getSpeed1())
#    sensor2.setAngle(sensorInput.getAngle2())
#    sensor2.setSpeed(sensorInput.getSpeed2())
    if pygame.key.get_pressed()[pygame.K_a]:
         sensor2.setAngle(-5)
    if pygame.key.get_pressed()[pygame.K_d]:
         sensor2.setAngle(5)
    if pygame.key.get_pressed()[pygame.K_w]:
        sensor2.setSpeed(1)
    if pygame.key.get_pressed()[pygame.K_s]:
        sensor2.setSpeed(-1)
    

def findCollision(bikePosition,bike,rival):
    if bike.prev_pos.__len__()-20 < 0:
        maxPos = 0
    elif rival:
        maxPos = bike.prev_pos.__len__()
    else:
        maxPos = bike.prev_pos.__len__()-20

    if bikePosition[0] < 0 or bikePosition[0] > screenSize[0] or bikePosition[1] < 0 or bikePosition[1] > screenSize[1]:
        return True

    for p in bike.prev_pos[:maxPos]:
        if abs(abs(p[0])-abs(bikePosition[0])) < 5 and abs(abs(p[1])-abs(bikePosition[1])) < 5:
            return True

    return False

class Sensors():
    def __init__(self):
        self.speed = 1
        self.angle = random.uniform(0,360)

    def setAngle(self, direction):
        self.angle += direction
        self.angle %= 360


    def setSpeed(self,acceleration):
        if acceleration > 0 and  self.speed < 10:
            self.speed += 1
        elif acceleration < 0 and  self.speed > 1:
            self.speed -= 1

    def reset(self):
        self.speed = 1
        self.angle = random.uniform(0,360)

Player1Start = 524
Player2Start = 512

class Sensors2():
    def __init__(self, playerNum):
        self.speed = 1
        self.angle = 0
        self.playerNum = playerNum

    def setAngle(self, direction):

        if (self.playerNum == 1):
            offset = Player1Start
        else:
            offset = Player2Start

        self.angle =  self.angle + (direction - offset)/34
        self.angle %= 360
        #print(direction)

    def setSpeed(self,acceleration):
        self.speed = max(acceleration/20 ,1)
        self.speed =  min (13, self.speed)



    def reset(self):
        self.speed = 1
        self.angle = 0


class Bike():
    def __init__(self,colors,sensors):
        self.xdir = random.uniform(100,screenSize[0]-100)
        self.ydir = random.uniform(100,screenSize[1]-100)
        self.prev_pos = []
        self.headcolor = colors[0]
        self.bodydcolor = colors[1]
        self.sensors = sensors
        self.score = 0

    def reset(self):
        self.prev_pos = []
        self.sensors.reset()
        self.xdir = random.uniform(100,screenSize[0]-100)
        self.ydir = random.uniform(100,screenSize[1]-100)

    def getPosition(self):
        return (self.xdir,self.ydir)

    def update(self):
        self.prev_pos.append((self.xdir,self.ydir))
        if len(self.prev_pos) > 4:
            pygame.draw.lines(screen, self.headcolor, False, self.prev_pos,7)
            #make the head of the snake, TODO
            line = pygame.draw.lines(screen, self.bodydcolor, False, self.prev_pos[:self.prev_pos.__len__()-3],7)

        self.xdir += self.sensors.speed * math.cos(math.radians(self.sensors.angle))
        self.ydir += self.sensors.speed * math.sin(math.radians(self.sensors.angle))

def getTextSize(text):
    return myfont.size(text)


def game(bike1,bike2):
#    sensorThread = threading.Thread(target=sensorInput.start_sensor, args = ())
#    sensorThread.daemon = True
#    sensorThread.start()
    clock = pygame.time.Clock()

    vlc_instance = vlc.Instance("no-one-instance --input-repeat=999999")

    media = vlc_instance.media_new('sound.mp3')
    player = vlc_instance.media_player_new()
    player.set_media(media)
    player.play()
    player.audio_set_volume(100)

    gameover = False
    roundNum = 0
    while True:
        clock.tick(300)
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        bgi = pygame.image.load(background)
        resizedBackground = pygame.transform.scale(bgi, (screenSize[0], screenSize[1]))

        #print(sensorInput.getAngle())
        if not gameover:
            screen.blit(resizedBackground, (0, 0))

            keyPress(bike1.sensors,bike2.sensors)
            bike1.update()
            bike2.update()

            Col = False
            # find if player1 collides with player2 or its own track
            Col = Col or  findCollision(bike1.getPosition(),bike1,False)
            Col = Col or findCollision(bike1.getPosition(),bike2,True)

            if(Col):
                print("player1 lose")
                bike2.score+=1
                gameover = True
                loose = 1

            Col = False
        # find if player2 collides with player1 or its own track
            Col = Col or findCollision(bike2.getPosition(),bike1,True)
            Col = Col or findCollision(bike2.getPosition(),bike2,False)

            if(Col):
                print("player2 lose")
                bike1.score+=1
                gameover = True
                loose = 2

        if gameover:

            loseText = "player"+ loose.__str__()+" lose"
            loseText_X_position = screenSize[0]/2 - (getTextSize(loseText))[0]/2
            screen.blit(myfont.render(loseText,1,(0,0,0)), (loseText_X_position, 300))

            press2Cont ="Press space to continue"
            press2Cont_X_possition = screenSize[0]/2 - (getTextSize(press2Cont))[0]/2
            screen.blit(myfont.render(press2Cont,1,(0,0,0)), (press2Cont_X_possition, 500))

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                gameover = False
                bike1.reset()
                bike2.reset()
                roundNum+=1
                if roundNum >= numOfTurns:
                    player.stop()
                    return END_GAME


        Xoffset = 20;

        player1Score = "player1 score:"+ bike1.score.__str__()
        player1Score_X_possition = Xoffset
        screen.blit(myfont.render(player1Score,1,(255,100,0)), (player1Score_X_possition, 20))

        player2Score = "player2 score:"+ bike2.score.__str__()
        player2Score_X_possition = screenSize[0] - (getTextSize(player2Score))[0] - Xoffset
        screen.blit(myfont.render(player2Score,1,(255,100,0)), (player2Score_X_possition, 20))

        roundNumText = "round: "+ (roundNum+1).__str__()
        roundNumText_X_possition = screenSize[0]/2 - (getTextSize(roundNumText))[0]/2
        screen.blit(myfont.render(roundNumText,1,(155,100,30)), (roundNumText_X_possition, 100))


        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return QUIT



        pygame.display.flip()



def menu():
    pygame.mouse.set_visible(True)
    bgi = pygame.image.load(background_menu)
    resizedBackground = pygame.transform.scale(bgi, (screenSize[0], screenSize[1]))
    screen.blit(resizedBackground, (0, 0))

    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        startText = "START GAME"
        startText_X_possition = 2*screenSize[0]/3 - (getTextSize(startText))[0]/2+100
        sng = screen.blit(maenuFont.render(startText,1,(155,100,30)), (startText_X_possition, 150))

        for ev in pygame.event.get():
            if sng.collidepoint(pygame.mouse.get_pos()):
                sng = screen.blit(maenuFont.render(startText,1,(55,100,30)), (startText_X_possition, 150))
                if ev.type == pygame.MOUSEBUTTONUP:
                    return NEW_GAME
        bgi = pygame.image.load(background)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return QUIT
        pygame.display.flip()


def main():

    while True:
        ret = menu()

        if ret == NEW_GAME:
            bike1 = Bike(player1Color,Sensors())
            bike2 = Bike(player2Color,Sensors())
            var = game(bike1,bike2)
        elif ret == QUIT:
            break;

    pygame.mouse.set_visible(True)
    sensorInput.stop()

if __name__ == "__main__":
    main()

        

