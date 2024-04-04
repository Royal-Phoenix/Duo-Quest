from pygame import mixer

mixer.init()
mixer.music.set_volume(0.7)

while True:
    mixer.music.load('assets/sounds/Device Connect.wav')
    mixer.music.play()
    for i in range(10000000):
        pass
    mixer.music.load('assets/sounds/Device Disconnect.wav')
    mixer.music.play()
    for i in range(10000000):
        pass
