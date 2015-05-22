#! /usr/bin/python
from unittest.case import _Outcome

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
MAX_SPEED = 30

screenX = 800
screenY = 600

SPEED_RADIUS = 123

screenSize = [screenX,screenY]

BlackBackground = 'BlackBackground.gif'
background_menu = 'Background.jpg'

out_of_sync = 'out_of_sync.gif'
awesome = 'awesome.gif'
pedal_faster = 'pedal_faster.gif'

screen = pygame.display.set_mode(screenSize)

myFont = pygame.font.SysFont("monospace", 30)
menuFont = pygame.font.SysFont("monospace", 70)

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

    while True:
        clock.tick(20)

        bgi = pygame.image.load(background_menu)
        resizedBackground = pygame.transform.scale(bgi, (screenX, screenY))
        screen.blit(resizedBackground, (0, 0))

        startText = "START GAME"
        startText_X_position = 2*screenX/3 - (getTextSize(startText))[0]/2+100
        sng = screen.blit(menuFont.render(startText,1,(155,100,30)), (startText_X_position, 150))


        for ev in pygame.event.get():
            if sng.collidepoint(pygame.mouse.get_pos()):
                sng = screen.blit(menuFont.render(startText,1,(55,100,30)), (startText_X_position, 150))
                if ev.type == pygame.MOUSEBUTTONUP:
                    return NEW_GAME


        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return QUIT
        pygame.display.flip()

