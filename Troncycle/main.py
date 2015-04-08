import pygame
import math
import time

pygame.init()

screen = pygame.display.set_mode((1000, 1003))


class Bike():
    def __init__(self,color1,color2,startx,starty):
        self.xdir = startx
        self.ydir = starty
        self.prev_pos = []
        self.speed = 1
        self.angle = 0
        self.headcolor = color1 #(0, 0, 255)
        self.bodydcolor = color2 #(255, 0, 0)

    def setAngle(self, direction):
        self.angle += direction
        self.angle %= 360

    def findCollision(self,position):
        if self.prev_pos.__len__()-20 < 0:
            maxPos = 0
        else:
            maxPos = self.prev_pos.__len__()-20

        for p in self.prev_pos[:maxPos]:
            if abs(abs(p[0])-abs(position[0])) < 5 and abs(abs(p[1])-abs(position[1])) < 5:
                print("collision!!!!")


    def update(self):
        self.prev_pos.append((self.xdir,self.ydir))
        if len(self.prev_pos) > 4:
            pygame.draw.lines(screen, self.headcolor, False, self.prev_pos,7)
            #make the head of the snake, TODO
            line = pygame.draw.lines(screen, self.bodydcolor, False, self.prev_pos[:self.prev_pos.__len__()-3],7)

        self.findCollision((self.xdir,self.ydir))


        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.setAngle(-5)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.setAngle(5)
        if pygame.key.get_pressed()[pygame.K_UP]:
            if self.speed < 10:
                self.speed += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.speed > 1:
                self.speed -= 1

        self.xdir += self.speed * math.cos(math.radians(self.angle))
        self.ydir += self.speed * math.sin(math.radians(self.angle))




def main():
    lb1 = Bike((0, 0, 255),(255, 0,0),50,50)
    lb2 = Bike((255, 0,0),(0, 0, 255), 500,500)
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if lb1.xdir >= screen.get_width():
          print("collision!")
        if lb1.ydir >= screen.get_width():
          print("collision!")

        bgi = pygame.image.load('BlackBackground.gif')
        screen.blit(bgi, (0, 0))

        lb1.update()
        lb2.update()
    #    Sprites.draw(screen)
        pygame.display.flip()

    # return mouse cursor
    pygame.mouse.set_visible(True)


if __name__ == "__main__":
    main()

        
