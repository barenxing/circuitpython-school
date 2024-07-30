import board, neopixel, digitalio

RED = (255, 0, 0)
BLACK = (0, 0, 0)

PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)

button_A = digitalio.DigialInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)

led_toggle = False


while True:
	if button_A.value:
		led_toggle = !led_toggle

	if led_toggle:
		pixels.fill(RED)
	else:
		pixels.fill(BLACK)

