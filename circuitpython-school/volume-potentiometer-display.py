# volume-potentiometer-display.py
import time

import board, neopixel
from time import sleep
from analogio import AnalogIn

from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, \
    BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK


def range_map(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    in_delta = in_max - in_min
    out_delta = out_max - out_min
    return int(value * out_delta / in_delta)


# setup color & neo pixels
colors = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK,
          AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK]

NUM_PIXELS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS)
pixels.brightness = 0.01  # at 0.01 some colors looks the same, use 0.1 or higher
BLINK_DELAY = 0.2

print("Rotate potentiometer to change volume")

# light up each light in a different color
pixels[:] = BLACK * NUM_PIXELS

potentiometer = AnalogIn(board.A3)
volume = 0

while True:
    # going over 10 becaue the value 11 is only reached when potentiometer.value is 65535
    # volume 0 all lights off, volume 10 all lights on.
    volume = range_map(potentiometer.value, 0, 65535, 0, 11)
    print(f"volume: {volume}")
    if not volume:
        pixels[:] = BLACK * NUM_PIXELS
    else:
        pixels[:] = [RED if i < volume else BLACK for i in range(NUM_PIXELS)]
    sleep(BLINK_DELAY)
