from time import sleep
import board, neopixel

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
RED     = (255,   0,   0)
ORANGE  = (255,  40,   0)
YELLOW  = (255, 150,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
INDIGO  = ( 75,   0, 130)
VIOLET  = (180,   0, 255)
WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)

COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET, WHITE, BLACK]
COLOR_COUNT = len(COLORS)
delay_time = 1 / 60

index = 0
pixels.fill(BLACK)
pixels.brightness = 0.05

while True:
    sleep(delay_time)
    pixels[PIXEL_COUNT - 1 - (index % PIXEL_COUNT)] = COLORS[index % COLOR_COUNT]
    index += 1

