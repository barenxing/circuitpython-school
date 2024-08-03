import board, neopixel
from time import sleep

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLINK_DELAY = 0.2

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
pixels.brightness = 0.05

while True:
    pixels.fill(RED)
    sleep(BLINK_DELAY)
    pixels.fill(BLACK)
    sleep(BLINK_DELAY)

