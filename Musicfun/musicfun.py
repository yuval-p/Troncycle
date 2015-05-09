__author__ = 'guy'
import sys
import vlc
import msvcrt
import _thread
import time
from tkinter import *

def setup_player():

    vlc_instance = vlc.Instance("no-one-instance")

    media = vlc_instance.media_new("1.mp3")
    player = vlc_instance.media_player_new()
    player.set_media(media)
    player.play()

    return player

def setup_noise():

    vlc_instance = vlc.Instance("no-one-instance --input-repeat=999999")

    media = vlc_instance.media_new("noise.wav")
    noise = vlc_instance.media_player_new()
    noise.set_media(media)
    noise.play()

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

    if (vel1 < 5 and vel2 < 5):
            noiseVolume = 10;

    print("noiseVolume: " + (str)(noiseVolume));
    return noiseVolume;

def main():
    print("Starting Musicfun...")
    #_thread.start_new_thread(keypress, ())

    root = Tk();
    root.title("Musicfun");
    root.geometry("640x480");

    root.mainloop();

    song = setup_player()
    noise = setup_noise()

    MaxVelocity = 30;

    vel1 = 0;
    vel2 = 0;

    #global char
    print("Waiting for input")

    while True:
        ch = ord(msvcrt.getch())
        #print(char)

        if (ch == 27):
            exit(0)
        elif ((ch == 87) or (ch == 119)):
            #IncreaseVolume(noise)
            vel1 = min(vel1 + 5, MaxVelocity);
        elif ((ch == 83) or (ch == 115)):
            #DecreaseVolume(noise)
            vel1 = max(vel1 - 5, 0);
        elif ch == 72:
            #IncreaseVolume(song)
            vel2 = min(vel2 + 5, MaxVelocity);
        elif ch == 80:
            #DecreaseVolume(song)
            vel2 = max(vel2 - 5, 0);
        time.sleep(0.05)

        print("vel1, vel2" + "(" + (str)(vel1) + ", " + (str)(vel2) + ")");
        songVol = (int)(CalcSongVolume(vel1, vel2));
        noiseVolume = (int)(CalcNoiseVolume(vel1, vel2));

        change_volume(song, songVol);
        change_volume(noise, noiseVolume);
main()