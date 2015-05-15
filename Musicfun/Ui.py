#! /usr/bin/python
__author__ = 'guy'
import pygame

pygame.init()

END_GAME = 1
QUIT = 2
NEW_GAME = 3

screenSize = [800,600]

background = 'tron-backgrounds.jpg'
background_menu = 'tron-menus.jpg'
screen = pygame.display.set_mode(screenSize)

myFont = pygame.font.SysFont("monospace", 30)
menuFont = pygame.font.SysFont("monospace", 70)

def getTextSize(text):
    return myFont.size(text)

def menu():
    pygame.mouse.set_visible(True)
    bgi = pygame.image.load(background_menu)
    screen.blit(bgi, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    while True:
        clock.tick(20)
        startText = "START GAME"
        startText_X_possition = 2*screenSize[0]/3 - (getTextSize(startText))[0]/2+100
        sng = screen.blit(menuFont.render(startText,1,(155,100,30)), (startText_X_possition, 150))

        for ev in pygame.event.get():
            if sng.collidepoint(pygame.mouse.get_pos()):
                sng = screen.blit(menuFont.render(startText,1,(55,100,30)), (startText_X_possition, 150))
                if ev.type == pygame.MOUSEBUTTONUP:
                    return NEW_GAME
        bgi = pygame.image.load(background)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return QUIT
        pygame.display.flip()

