__author__ = 'guy'
import vlc

def setup_player():

    vlc_instance = vlc.Instance("no-one-instance")

    media = vlc_instance.media_new("1.mp3")
    player = vlc_instance.media_player_new()
    player.set_media(media)
    player.play()

    return player

def setup_noise():

    vlc_instance = vlc.Instance("no-one-instance --input-repeat=999999")

    media = vlc_instance.media_new("Oz.wma")
    noise = vlc_instance.media_player_new()
    noise.set_media(media)
    noise.play()

    return noise

def change_volume(player, vol):
    player.audio_set_volume(vol)