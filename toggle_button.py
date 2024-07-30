import board, neopixel, digitalio

RED = (255, 0, 0)
BLACK = (0, 0, 0)

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.05

button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)

button_state = True
led_toggle = False


while True:
    if button_A.value and button_state:
        led_toggle = not led_toggle
        button_state = False

    if not button_A.value:
        button_state = True

    pixels.fill(RED if led_toggle else BLACK)
