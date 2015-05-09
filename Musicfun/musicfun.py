__author__ = 'guy'
import sys
import vlc
import msvcrt
import _thread
import time
import random
import pygame
import math

pygame.init()

#settings
screenSize = [800,600]

background = 'tron-backgrounds.jpg'
background_menu = 'tron-menus.jpg'


END_GAME = 1
QUIT = 2
NEW_GAME = 3

myfont = pygame.font.SysFont("monospace", 30)
maenuFont = pygame.font.SysFont("monospace", 70)

screen = pygame.display.set_mode(screenSize)

def setup_player():

    vlc_instance = vlc.Instance("no-one-instance")

    media = vlc_instance.media_new("1.mp3")
    player = vlc_instance.media_player_new()
    player.set_media(media)
    player.play()

    player.audio_set_volume(0)

    return player

def setup_noise():

    vlc_instance = vlc.Instance("no-one-instance --input-repeat=999999")

    media = vlc_instance.media_new("noise.wav")
    noise = vlc_instance.media_player_new()
    noise.set_media(media)
    noise.play()

    noise.audio_set_volume(0)

    return noise

def change_volume(player, vol):
    player.audio_set_volume(vol)

def IncreaseVolume(player):
    vol = player.audio_get_volume();
    print(vol)
    newVolume = min(vol + 5, 200);
    player.audio_set_volume(newVolume)

def DecreaseVolume(player):
    vol = player.audio_get_volume();
    print(vol)
    newVolume = max(vol - 5, 0);
    player.audio_set_volume(newVolume)

def CalcSongVolume(vel1, vel2):
    MaxVelocity = 30;
    avgVel = (vel1 + vel2)/2;

    songVolume = avgVel/MaxVelocity*200;
    print("songVolume: " + (str)(songVolume));
    return songVolume;

def CalcNoiseVolume(vel1, vel2):
    MaxVelocity = 30;
    gap = abs(vel1 - vel2);

    print("gap: " + (str)(gap));
    correlation = gap/MaxVelocity;

    noiseVolume = correlation*200;

    if (vel1 <= 5 and vel2 <= 5):
            noiseVolume = 50;

    print("noiseVolume: " + (str)(noiseVolume));
    return noiseVolume;

# TODO change to the sensors input..
def keyPress(sensor1,sensor2):
    SpeedChange = 1

    if pygame.key.get_pressed()[pygame.K_LEFT]:
         sensor1.setAngle(-5)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
         sensor1.setAngle(5)
    if pygame.key.get_pressed()[pygame.K_UP]:
        sensor1.SetSpeed(sensor1.Speed + SpeedChange)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        sensor1.SetSpeed(sensor1.Speed - SpeedChange)
    if pygame.key.get_pressed()[pygame.K_a]:
         sensor2.setAngle(-5)
    if pygame.key.get_pressed()[pygame.K_d]:
         sensor2.setAngle(5)
    if pygame.key.get_pressed()[pygame.K_w]:
        sensor2.SetSpeed(sensor2.Speed + SpeedChange)
    if pygame.key.get_pressed()[pygame.K_s]:
        sensor2.SetSpeed(sensor2.Speed - SpeedChange)

class Sensors():
    def __init__(self):
        self.Speed = 0
        self.Angle = 0
        self.MaxSpeed = 30

    def SetAngle(self, direction):
        self.Angle += direction
        self.Angle %= 360

    def SetSpeed(self, newSpeed):
        self.Speed = newSpeed
        self.Speed = min(self.Speed, self.MaxSpeed)
        self.Speed = max(self.Speed, 0)

    def reset(self):
        self.Speed = 0
        self.angle = random.uniform(0,360)

class Bike():
    def __init__(self, sensors):
        self.sensors = sensors

def getTextSize(text):
    return myfont.size(text)


def game(bike1,bike2):
    clock = pygame.time.Clock()
    roundNum = 0

    song = setup_player()
    noise = setup_noise()

    while True:
        clock.tick(20)
        # pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        bgi = pygame.image.load(background)
        screen.blit(bgi, (0, 0))

        keyPress(bike1.sensors,bike2.sensors)

        print("vel1, vel2" + "(" + (str)(bike1.sensors.Speed) + ", " + (str)(bike2.sensors.Speed) + ")");
        songVolume = (int)(CalcSongVolume(bike1.sensors.Speed, bike2.sensors.Speed));
        noiseVolume = (int)(CalcNoiseVolume(bike1.sensors.Speed, bike2.sensors.Speed));

        change_volume(song, songVolume);
        change_volume(noise, noiseVolume);


        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return QUIT

        pygame.display.flip()



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
            bike1 = Bike(Sensors())
            bike2 = Bike(Sensors())
            var = game(bike1,bike2)
        elif ret == QUIT:
            break;

    pygame.mouse.set_visible(True)


if __name__ == "__main__":
    main()


