# print plot

import board, neopixel, digitalio, analogio
from time import sleep
from adafruit_led_animation.color import BLACK, GREEN, RED
from adafruit_debouncer import Button

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.1
pixels.fill(BLACK)

light_sensor = analogio.AnalogIn(board.LIGHT)

button_A_pin = digitalio.DigitalInOut(board.BUTTON_A)
button_A_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(button_A_pin, value_when_pressed=True)

button_B_pin = digitalio.DigitalInOut(board.BUTTON_B)
button_B_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(button_B_pin, value_when_pressed=True)

run_plot = False

DELAY_TIME = 0.1

def blink(p_index, color, delay):
    pixels[p_index] = color
    sleep(delay)
    pixels[p_index] = BLACK


def vmap(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    in_delta = in_max - in_min
    out_delta = out_max - out_min
    return int(value * out_delta / in_delta)


print("Press Button A to start plotting light sensor value, press Button B to stop.")
while True:
    button_A.update()
    button_B.update()

    if button_B.pressed:
        run_plot = False
        print("Stopping plot")
        blink(7, RED, DELAY_TIME)
    elif button_A.pressed:
        run_plot = True
        print("starting plot")
        blink (2, GREEN, DELAY_TIME)

    bar_height = vmap(light_sensor.value, 500, 65536, 0, 99)
    print(' ' * bar_height + f'* ({bar_height})')
    sleep(0.2)

