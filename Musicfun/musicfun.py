__author__ = 'guy'
import sys
import _thread
import time
import pygame
import threading

import AudioController
import Bike
import Sensors
import Ui
import tst

import math

sensorInput = tst.sensor_input()

def CalcSongVolume(vel1, vel2):
    MaxVelocity = 30;
    avgVel = (vel1 + vel2)/2;

    songVolume = avgVel/MaxVelocity*200;
    #print("songVolume: " + (str)(songVolume));
    return songVolume;

def CalcNoiseVolume(vel1, vel2):
    MaxVelocity = 30;
    gap = abs(vel1 - vel2);

    #print("gap: " + (str)(gap));
    correlation = gap/MaxVelocity;

    noiseVolume = correlation*200;

    if (vel1 <= 5 and vel2 <= 5):
            noiseVolume = 50;

    #print("noiseVolume: " + (str)(noiseVolume));
    return noiseVolume;

# TODO change to the sensors input..
def keyPress(sensor1,sensor2):
    SpeedChange = 1

    #if pygame.key.get_pressed()[pygame.K_LEFT]:
    #     sensor1.setAngle(-5)
    #if pygame.key.get_pressed()[pygame.K_RIGHT]:
    #     sensor1.setAngle(5)
    #if pygame.key.get_pressed()[pygame.K_UP]:
    #    sensor1.SetSpeed(sensor1.Speed + SpeedChange)
    #if pygame.key.get_pressed()[pygame.K_DOWN]:
    #    sensor1.SetSpeed(sensor1.Speed - SpeedChange)
    #if pygame.key.get_pressed()[pygame.K_a]:
    #     sensor2.setAngle(-5)
    #if pygame.key.get_pressed()[pygame.K_d]:
    #     sensor2.setAngle(5)
    #if pygame.key.get_pressed()[pygame.K_w]:
    #    sensor2.SetSpeed(sensor2.Speed + SpeedChange)
    #if pygame.key.get_pressed()[pygame.K_s]:
    #    sensor2.SetSpeed(sensor2.Speed - SpeedChange)


    sensor1.SetAngle(sensorInput.getAngle1())
    sensor1.SetSpeed(sensorInput.getSpeed1()*2*math.pi*60*30/(1000* 100))
    sensor2.SetAngle(sensorInput.getAngle2())
    sensor2.SetSpeed(sensorInput.getSpeed2()*2*math.pi*60*32/(1000* 100))

    #print(sensorInput.getSpeed1())

def feedback(songVolume, noiseVolume):
    if noiseVolume > 80:
        return Ui.out_of_sync
    if songVolume > 170:
        return Ui.awesome
    return Ui.pedal_faster

def game(bike1,bike2):
    sensorThread = threading.Thread(target=sensorInput.start_sensor, args = ())
    sensorThread.daemon = True
    sensorThread.start()
    clock = pygame.time.Clock()
    roundNum = 0

    song = AudioController.setup_player()
    noise = AudioController.setup_noise()

    t = 0

    while True:
        clock.tick(20)
        # pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        bgi = pygame.image.load(Ui.BlackBackground)
        #resizedBackground = pygame.transform.scale(bgi, (Ui.screenX, Ui.screenY))
        Ui.screen.blit(bgi, (0, 0))

        keyPress(bike1.sensors,bike2.sensors)

        #print("vel1, vel2" + "(" + (str)(bike1.sensors.Speed) + ", " + (str)(bike2.sensors.Speed) + ")");

        Ui.draw_player_speed("player1", Ui.RED, (int)(Ui.screenX/4),(int)(Ui.screenY*5/6),bike1.sensors.Speed,Ui.screen)
        Ui.draw_player_speed("player2", Ui.GREEN, (int)(Ui.screenX*3/4),(int)(Ui.screenY*5/6),bike2.sensors.Speed,Ui.screen)

        songVolume = (int)(CalcSongVolume(bike1.sensors.Speed, bike2.sensors.Speed));
        noiseVolume = (int)(CalcNoiseVolume(bike1.sensors.Speed, bike2.sensors.Speed));

        if ((int)(t / 10)) % 2 == 0:
            feedbackImage = feedback(songVolume, noiseVolume)
            Ui.draw_feedback(feedbackImage)

        t+=1

        AudioController.change_volume(song, songVolume);
        AudioController.change_volume(noise, noiseVolume);


        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return Ui.QUIT

        pygame.display.flip()



def main():

    while True:
        ret = Ui.menu()

        if ret == Ui.NEW_GAME:
            bike1 = Bike.Bike(Sensors.Sensors())
            bike2 = Bike.Bike(Sensors.Sensors())
            var = game(bike1,bike2)
        elif ret == Ui.QUIT:
            break;

    pygame.mouse.set_visible(True)


if __name__ == "__main__":
    main()


