# plotting wtih the Accelerometer
# https://youtu.be/1sfp30BfbUQ?si=vP18USM3NAN7ZkMO

import board, neopixel, busio, adafruit_lis3dh, digitalio, analogio
from time import sleep
from adafruit_led_animation.color import BLACK, GREEN, RED
from adafruit_debouncer import Button

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# set range
accelerometer.range = adafruit_lis3dh.RANGE_2_G

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.1
pixels.fill(BLACK)

# light_sensor = analogio.AnalogIn(board.LIGHT)


button_A_pin = digitalio.DigitalInOut(board.BUTTON_A)
button_A_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(button_A_pin, value_when_pressed=True)

button_B_pin = digitalio.DigitalInOut(board.BUTTON_B)
button_B_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(button_B_pin, value_when_pressed=True)

run_plot = False

BLINK_DELAY_TIME = 0.1
LOOP_DELAY_TIME = 0.2

def blink(p_index, color, delay):
    pixels[p_index] = color
    sleep(delay)
    pixels[p_index] = BLACK


def vmap(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    in_delta = in_max - in_min
    out_delta = out_max - out_min
    return int(value * out_delta / in_delta)


print("Press Button A to start plotting sensor value, press Button B to stop.")
while True:
    button_A.update()
    button_B.update()

    if button_B.pressed:
        run_plot = False
        print("Stopping plot")
        blink(7, RED, BLINK_DELAY_TIME)
    elif button_A.pressed:
        run_plot = True
        print("starting plot")
        blink (2, GREEN, BLINK_DELAY_TIME)

    if run_plot:
        # bar_height = vmap(light_sensor.value, 500, 65536, 0, 99)
        # print(' ' * bar_height + f'* ({bar_height})')
    
        x, y, z = accelerometer.acceleration
        # print((x, y, z)) # for plotting with Mu Editor
        print(f"x:{x:6.2f}, y:{y:6.2f}, z:{z:6.2f}")
        sleep(LOOP_DELAY_TIME)

