import pygame
import math
import time

pygame.init()

screen = pygame.display.set_mode((1000,1003))

class LightBike(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cycle.gif')
        self.rect = self.image.get_rect()
        self.prev_pos = []
        self.speed = 1
        self.x = 0.0
        self.y = 0.0
        self.angel = 0
        
    def update(self):

        self.prev_pos.append(self.rect.center)
        if len(self.prev_pos) > 1:
            pygame.draw.aalines(screen,(0,0,255),False,self.prev_pos)
             
        #if len(self.prev_pos) > 100:
         #   self.prev_pos.pop(0)
            
    #    if pygame.key.get_pressed()[pygame.K_RIGHT]
                
        self.image = pygame.image.load('cycle.gif')
                    
        if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.slowdown()
            #    self.image = pygame.image.load('light4.gif')
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.setAngel(5)
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.setAngel(-5)
                print("hello!")
          #      print(self.angel)
             #   self.image = pygame.image.load('light2.gif')
        elif pygame.key.get_pressed()[pygame.K_UP]:
                self.speedup()
              #  self.image = pygame.image.load('light1.gif')

        if self.angel < 90:
            print("<90")
        elif self.angel < 180 :
            print("<180")
        elif self.angel < 270 :
            print("<270")
        elif self.angel < 360 :
            print("<360")


        self.x = self.speed*math.cos(math.radians(self.angel))
        self.y = self.speed*math.sin(math.radians(self.angel))
        self.rect.centery += self.y
        self.rect.centerx += self.x
    #    print(self.rect.centerx)
        #print(self.y)


    def setAngel(self,direction):
        self.angel += direction
        self.angel %= 360

    #    print(self.angel)
       # self.x += self.speed*math.cos(self.angel)
       # self.y += self.speed*math.sin(self.angel)

    def slowdown(self):
        self.speed -= 1
    def speedup(self):
        self.speed += 1


        
    
        
        
def main():
    lb = LightBike()
    Sprites = pygame.sprite.Group(lb)
    clock = pygame.time.Clock()
    while True:
        clock.tick(500)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        if lb.rect.centery >= screen.get_width():
            lb.rect.centery = screen.get_width()
        if lb.rect.centerx >= screen.get_width():
            lb.rect.centerx = screen.get_width()
        if lb.rect.centery <= 0:
            lb.rect.centery = 0
        if lb.rect.centerx <= 0:
            lb.rect.centerx = 0
        bgi = pygame.image.load('BlackBackground.gif')
        screen.blit(bgi,(0,0))
        
        Sprites.update()
        Sprites.draw(screen)
        pygame.display.flip()
    
    #return mouse cursor
    pygame.mouse.set_visible(True)
    

if __name__ == "__main__":
    main()

        
