#! /usr/bin/python
from unittest.case import _Outcome

import SongsMenu

__author__ = 'guy'
import pygame
import math
import Sensors
from pygame import gfxdraw

from math import pi
pygame.init()

END_GAME = 1
QUIT = 2
NEW_GAME = 3


RED =   (255,   0,   0)
GREEN =   (0,   255,   0)
BLACK =   (0,   0,   0)
BLUE = (0,0,255)
MAX_SPEED = 40

screenX = 1280
screenY = 768

SPEED_RADIUS = 123

screenSize = [screenX,screenY]

BlackBackground = 'BlackBackground.gif'
background_menu = 'Background.jpg'

out_of_sync = 'out_of_sync.gif'
awesome = 'awesome.gif'
pedal_faster = 'pedal_faster.gif'

screen = pygame.display.set_mode(screenSize,pygame.FULLSCREEN)
#screen = pygame.display.set_mode(screenSize)

myFont = pygame.font.SysFont("monospace", 30)
menuFont = pygame.font.SysFont("monospace", 40)

def getTextSize(text):
    return myFont.size(text)

def speed_tp_pi(speed):
    #max speed is 30
    ratio = speed / MAX_SPEED
    degree = ratio * 360
    return pi - math.radians(degree)

def speed_to_degree(speed):
    #max speed is 30
    return 180+int(speed/MAX_SPEED*180)

def draw_speed(color, pos_x,pos_y,speed,screen, radius):
    for r in range(radius-10,radius):
        pygame.gfxdraw.arc(screen,pos_x,pos_y,r,180,speed_to_degree(speed),color)


def draw_player_speed(player, color, pos_x, pos_y, speed, screen):
    speedText = player + " speed"
    sng = screen.blit(myFont.render(speedText,1,color), (pos_x - SPEED_RADIUS, pos_y + 20))
    draw_speed(color, pos_x,pos_y,speed,screen, SPEED_RADIUS)

    ones = ((int)(speed) % 10)
    tens = (int)(speed / 10)

    AspectRatio = 122/90;

    width = (int)(SPEED_RADIUS/2)
    height = (int)(width*AspectRatio)
    drawDigit(player, tens, pos_x - width, pos_y - height, width, height)
    drawDigit(player, ones, pos_x, pos_y - height, width, height)

def drawDigit(player, digit, posX, posY, width, height):
    digitImage = getDigitImage(player, digit);
    im = pygame.image.load(digitImage)
    resizedImage = pygame.transform.scale(im, (width, height))
    screen.blit(resizedImage, (posX, posY))


def getDigitImage(player, digit):
    return (str)(digit) + "-" + player + ".png"

def draw_feedback(feedback_image):
    bgi = pygame.image.load(feedback_image);
    screen.blit(bgi, ((int)(screenX/4), (int)(screenY/3)));

def menu():
    pygame.mouse.set_visible(True)
    bgi = pygame.image.load(background_menu)
    resizedBackground = pygame.transform.scale(bgi, (screenX, screenY))
    screen.blit(resizedBackground, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()

    menu = SongsMenu.Menu()#necessary
    menu.init(['David Guetta - Dangerous', 'enrique iglesias - Bailando', 'Eurovision - Golden Boy',
               'Flo Rida -  The Gemini and Lookas', 'Flo Rida - Whistle', 'Jess Glynne - Hold My Hand',
               'Let It Happen - Tame Impala', 'Mark Ronson - Uptown Funk ft. Bruno Mars', 'Mark Ronson - I Cant Lose',
               'Meghan Trainor - All About That Bass', 'Michael Jackson, Justin Timberlake - Love Never Felt So Good',
               'Omer Adam feat. Arisa - Tel Aviv', 'Pitbull - Timber ft. Kesha', 'Rihanna, Kanye West, Paul McCartney - FourFiveSeconds',
               'Sia - Chandelier', 'Skazi - Hit n run', 'The Call - The Backstreet Boys'], screen)
    menu.draw()#necessary

    pygame.display.update()
    while True:
        clock.tick(20)

        bgi = pygame.image.load(background_menu)
        resizedBackground = pygame.transform.scale(bgi, (screenX, screenY))
        screen.blit(resizedBackground, (0, 0))

        startText = "Choose a song!"
        startText_X_position = screenX/3 - (getTextSize(startText))[0]/2+100
        sng = screen.blit(menuFont.render(startText,1,(155,100,30)), (startText_X_position, 150))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.draw(-1)
                if event.key == pygame.K_DOWN:
                    menu.draw(1)
                if event.key == pygame.K_RETURN:
                    menu.selected_song = menu.list[menu.get_position()]
                    return menu.selected_song
                if event.key == pygame.K_ESCAPE:
                    return QUIT
                pygame.display.update()
            elif event.type == pygame.QUIT:
                return QUIT

        pygame.time.wait(8)

