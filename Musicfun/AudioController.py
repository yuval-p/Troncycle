#! /usr/bin/python
__author__ = 'guy'

import vlc

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
