import random
import pygame
import math
import time

pygame.init()

myfont = pygame.font.SysFont("monospace", 30)

screen = pygame.display.set_mode([1000, 1000])

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


    if pygame.key.get_pressed()[pygame.K_a]:
         sensor2.setAngle(-5)
    if pygame.key.get_pressed()[pygame.K_d]:
         sensor2.setAngle(5)
    if pygame.key.get_pressed()[pygame.K_w]:
        sensor2.setSpeed(1)
    if pygame.key.get_pressed()[pygame.K_s]:
        sensor2.setSpeed(-1)


def findCollision(bikePosition,bike):
    if bike.prev_pos.__len__()-20 < 0:
        maxPos = 0
    else:
        maxPos = bike.prev_pos.__len__()-20
    for p in bike.prev_pos[:maxPos]:
        if abs(abs(p[0])-abs(bikePosition[0])) < 5 and abs(abs(p[1])-abs(bikePosition[1])) < 5:
         #   print("collision!!!!")
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



class Bike():
    def __init__(self,color1,color2,playerNum,sensors):
        self.xdir = random.uniform(1,500)
        self.ydir = random.uniform(1,500)
        self.prev_pos = []
        self.headcolor = color1 #(0, 0, 255)
        self.bodydcolor = color2 #(255, 0, 0)
        self.sensors = sensors
        self.score = 0

    def reset(self):
        self.prev_pos = []
        self.sensors.reset()
        self.xdir = random.uniform(1,500)
        self.ydir = random.uniform(1,500)

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


def game(bike1,bike2):
    clock = pygame.time.Clock()
    gameover = False
    while True:
        clock.tick(20)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if bike1.xdir >= screen.get_width():
          print("collision!")
        if bike1.ydir >= screen.get_width():
          print("collision!")

        bgi = pygame.image.load('BlackBackground.gif')
        screen.blit(bgi, (0, 0))
        if not gameover:
            keyPress(bike1.sensors,bike2.sensors)
            bike1.update()
            bike2.update()

            Col = False
            # find if player1 collides with player2 or its own track
            Col = Col or  findCollision(bike1.getPosition(),bike1)
            Col = Col or findCollision(bike1.getPosition(),bike2)

            if(Col):
                print("player1 lose")
                bike2.score+=1
                gameover = True
                loose = 1

            Col = False
        # find if player2 collides with player1 or its own track
            Col = Col or findCollision(bike2.getPosition(),bike1)
            Col = Col or findCollision(bike2.getPosition(),bike2)

            if(Col):
                print("player2 lose")
                bike1.score+=1
                gameover = True
                loose = 2

        if gameover:
            loseText = myfont.render("player"+ loose.__str__()+" lose", 1, (255,255,0))
            screen.blit(loseText, (500, 100))
            press2Cont = myfont.render("Press space to continue", 1, (255,255,0))
            screen.blit(press2Cont, (500, 500))
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                gameover = False
                bike1.reset()
                bike2.reset()

        player1Score = myfont.render("player1 score:"+ bike1.score.__str__(), 1, (255,100,0))
        screen.blit(player1Score, (100, 20))
        player2Score = myfont.render("player2 score:"+ bike2.score.__str__(), 1, (255,100,0))
        screen.blit(player2Score, (700, 20))

        pygame.display.flip()



def main():
    bike1 = Bike((0, 0, 255),(255, 0,0),1,Sensors())
    bike2 = Bike((255, 0,0),(0, 0, 255),2,Sensors())
    game(bike1,bike2)

    pygame.mouse.set_visible(True)




if __name__ == "__main__":
    main()

        
