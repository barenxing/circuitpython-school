# volume-button-display.py
import board, neopixel, digitalio
from adafruit_debouncer import Button
from time import sleep

from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, \
    BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK

# setup color & neo pixels
colors = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK,
          AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK]

NUM_PIXELS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS)
pixels.brightness = 0.01  # at 0.01 some colors looks the same, use 0.1 or higher
BLINK_DELAY = 0.2

print("Press Button A to increase, Press Button B to decrease")

# light up each light in a different color
pixels[:] = BLACK * NUM_PIXELS

button_A_input = digitalio.DigitalInOut(board.BUTTON_A)
button_A_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(pin=button_A_input, value_when_pressed=True)

button_B_input = digitalio.DigitalInOut(board.BUTTON_B)
button_B_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(pin=button_B_input, value_when_pressed=True)

volume = 0

while True:
    button_A.update()
    button_B.update()

    # if button_A.pressed:
    #     pixels[volume] = RED
    #     volume = min(volume + 1, NUM_PIXELS - 1)
    #     print(f"volume: {volume}")
    # elif button_B.pressed:
    #     pixels[volume] = BLACK
    #     volume = max(volume - 1, 0)
    #     print(f"volume: {volume}")

    if button_A.pressed:
        if volume < NUM_PIXELS:
            volume = volume + 1
            pixels[0:volume] = RED * volume
            pixels[volume:] = BLACK * (NUM_PIXELS-volume)
            print(f"volume: {volume}")
    elif button_B.pressed:
        if volume > 0:
            volume = volume - 1
            pixels[0:volume] = RED * volume
            pixels[volume:] = BLACK * (NUM_PIXELS-volume)
            print(f"volume: {volume}")
