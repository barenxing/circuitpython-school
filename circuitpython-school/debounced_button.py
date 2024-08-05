from time import sleep
import board, neopixel, digitalio
from adafruit_debouncer import Button
from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, \
    TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, \
    OLD_LACE, WHITE, BLACK
from audiocore import WaveFile
from audioio import AudioOut

speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

audio = AudioOut(board.SPEAKER)
path = "drumSounds/"
filename = "drum_cowbell.wav"



PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
INDIGO  = ( 75,   0, 130)
VIOLET  = (180,   0, 255)

COLORS = [
    RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA,
    GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK
]

delay_time = 0.5

pixels.fill(BLACK)
pixels.brightness = 0.05

button_A_input = digitalio.DigitalInOut(board.BUTTON_A)
button_A_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(pin=button_A_input, value_when_pressed=True)


button_B_input = digitalio.DigitalInOut(board.BUTTON_B)
button_B_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(pin=button_B_input, value_when_pressed=True)

while True:
    button_A.update()
    button_B.update()
    if button_A.pressed:
        pixels.fill(BLUE)
    elif button_A.released:
        pixels.fill(BLACK)
    if button_B.pressed:
        pixels.fill(RED)
        with open(path + filename, 'rb') as wave_file:
            wave = WaveFile(wave_file)
            audio.play(wave)
            while audio.playing:
                pass
    elif button_B.released:
        pixels.fill(BLACK)