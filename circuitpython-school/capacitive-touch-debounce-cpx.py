# capacitive-touch-debounce-cpx.py
# https://youtu.be/eEHOYggqa6U?si=RUVEAbw4Ri_AOPj8

import board, neopixel, digitalio, analogio, touchio
from time import sleep
from adafruit_led_animation.color import BLACK, RED, BLUE, YELLOW, AMBER, GREEN, CYAN, ORANGE
from adafruit_debouncer import Button
from audiocore import WaveFile
from audioio import AudioOut

# speaker setup
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

# use speaker location to create an Audio object
audio = AudioOut(board.SPEAKER)
path = "drumSounds/"


PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.01
pixels.fill(BLACK)

colors = [RED, BLUE, YELLOW, AMBER, GREEN, CYAN, ORANGE]
drumsamples = ['splat', 'scratch', 'bd_zome', 'drum_cowbell', 'elec_cymbal', 'elec_hi_snare', 'bass_hit_c']

# setup touch pads
touchpads = []
for pin in ([board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.A7]):
    touchpad_input = touchio.TouchIn(pin)
    touchpads.append(Button(touchpad_input, value_when_pressed=True))


def play_sound(filename):
    with open(path+filename, 'rb') as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

print("Touch pads A1 -> A7 to play drum sound")
while True:
    for i, touchpad in enumerate(touchpads):
        touchpad.update()
        if touchpad.pressed:
            pixels.fill(colors[i])
            play_sound(drumsamples[i]+".wav")
            pixels.fill(BLACK)

