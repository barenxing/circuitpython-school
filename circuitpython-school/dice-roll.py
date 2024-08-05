# dice-roll.py
# randomly lit up the pixels then end in a dice number
#
# https://youtu.be/lfjwD9D5Dws?si=K66oWbZtW1z1znQA
import random

import board, neopixel, digitalio, adafruit_lis3dh, busio, analogio, touchio
from random import randint
from time import sleep
from adafruit_led_animation.color import BLACK, WHITE, RED
from audiocore import WaveFile
from audioio import AudioOut

# speaker setup
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

# use speaker location to create an Audio object
audio = AudioOut(board.SPEAKER)
path = "drumSounds/"

# accelerometer setup
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# set range
accelerometer.range = adafruit_lis3dh.RANGE_2_G

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.01
pixels.fill(BLACK)
pixel_light_delay = 0.1

# setup touch pads
pads = [board.A1, board.A2, board.A3, board.A4, board.A5, board.A6, board.A7]
touchpads = []
dice_dots = [1, 2, 3, 6, 7, 8] # 3 on each side evenly spaced

for pad in pads:
    touchpads.append(touchio.TouchIn(pad))

def play_sound(filename):
    with open(path+filename, 'rb') as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pdx = randint(0, PIXEL_COUNT - 1)
            pixels[pdx] = WHITE
            sleep(pixel_light_delay)
            pixels[pdx] = BLACK

print("Shake CircuitPlayground or touch any of the pads to roll the dice")
random.seed(int(accelerometer.acceleration.x))

while True:
    for touchpad in touchpads:
        if touchpad.value or (accelerometer.acceleration.x > 16.0):
            pixels.fill(BLACK)
            sleep(pixel_light_delay)
            play_sound("scratch.wav")

            die_value = randint(1, 6)
            for i in range(die_value):
                pixels[dice_dots[i]] = RED
                sleep(pixel_light_delay)