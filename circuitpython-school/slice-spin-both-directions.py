# slice-spin-both-directions.py
import board, neopixel, digitalio
from adafruit_debouncer import Button
from time import sleep

from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, \
    BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK

# setup color & neo pixels
colors = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK,
          AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK]

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)
pixels.brightness = 0.01  # at 0.01 some colors looks the same, use 0.1 or higher
BLINK_DELAY = 0.2

print("Press Button A to spin clockwise, Press Button B to spin counterclockwise")

# light up each light in a different color
pixels[:] = colors[:len(pixels)]

NO_SPIN, CLOCKWISE, COUNTER_CLOCKWISE = range(3)

button_A_input = digitalio.DigitalInOut(board.BUTTON_A)
button_A_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(pin=button_A_input, value_when_pressed=True)

button_B_input = digitalio.DigitalInOut(board.BUTTON_B)
button_B_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(pin=button_B_input, value_when_pressed=True)

spin_direction = NO_SPIN

while True:
    button_A.update()
    button_B.update()
    if button_A.pressed:
        print("Button A is pressed")
        spin_direction = CLOCKWISE
    elif button_B.pressed:
        print("Button B is pressed")
        spin_direction = COUNTER_CLOCKWISE

    # based on the spin direction, rotate the LED
    if spin_direction == CLOCKWISE:
        temp_value = pixels[0]
        pixels[:-1] = pixels[1:]
        pixels[-1] = temp_value
        sleep(BLINK_DELAY)
    elif spin_direction == COUNTER_CLOCKWISE:
        temp_value = pixels[-1]
        pixels[1:] = pixels[:-1]
        pixels[0] = temp_value
        sleep(BLINK_DELAY)
