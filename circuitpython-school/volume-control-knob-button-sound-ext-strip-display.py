# volume-control-knob-button-sound-ext-strip-display.py

import board, neopixel, digitalio, touchio
from time import sleep
from analogio import AnalogIn
from adafruit_debouncer import Button
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

from adafruit_led_animation.color import RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, \
    BLUE, PURPLE, MAGENTA, GOLD, PINK, AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK

speaker_pin = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_pin.direction = digitalio.Direction.OUTPUT
speaker_pin.value = True

audio = AudioOut(board.SPEAKER)
PATH = "drumSounds/"
button_sound_file = "clap.wav"
knob_sound_file = "two_crickets.wav"

def play_sound(filename: str) -> None:
    with open(PATH+filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass


def range_map(value: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
    in_delta = in_max - in_min
    out_delta = out_max - out_min
    return int(value * out_delta / in_delta)


# setup color & neo pixels
colors = [RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, GOLD, PINK,
          AQUA, JADE, AMBER, OLD_LACE, WHITE, BLACK]

NUM_PIXELS = 10
NUM_STRIP_PIXELS = 8
MAX_VOLUME = min(NUM_PIXELS, NUM_STRIP_PIXELS)
BRIGHTNESS = 0.01
BLINK_DELAY = 0.2

pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=True)
strip_pixels = neopixel.NeoPixel(board.A1, NUM_STRIP_PIXELS, brightness=BRIGHTNESS, auto_write=True)

# light up each light in a different color
pixels[:] = BLACK * NUM_PIXELS
strip_pixels[:] = BLACK * NUM_STRIP_PIXELS

# setup potentiometer
potentiometer = AnalogIn(board.A3)

# setup buttons without debounce
button_A = digitalio.DigitalInOut(board.BUTTON_A)
button_A.switch_to_input(pull=digitalio.Pull.DOWN)

button_B = digitalio.DigitalInOut(board.BUTTON_B)
button_B.switch_to_input(pull=digitalio.Pull.DOWN)

touchpad_A2_input = touchio.TouchIn(board.A2)
touchpad_A2 = Button(touchpad_A2_input, value_when_pressed=True)

use_button_for_control = True  # defaults to use buttons as the volume control
print("Using Button for volume adjustment")
print("Press Button A to increase volume, Press Button B to decrease volume")
# print("Rotate potentiometer to change volume")
last_volume = 0
volume = 0

while True:
    touchpad_A2.update()
    if touchpad_A2.pressed:
        use_button_for_control = not use_button_for_control
        if use_button_for_control:
            play_sound(button_sound_file)
            print("Using Button for volume adjustment")
        else:
            play_sound(knob_sound_file)
            print("Using Knob for volume adjustment")

    if use_button_for_control:
        if volume < MAX_VOLUME and button_A.value:
            last_volume = volume
            volume = volume + 1
        elif volume > 0 and button_B.value:
            last_volume = volume
            volume = volume - 1
    else:  # use potentiometer for volume control
        # going over 10 becaue the value 11 is only reached when potentiometer.value is 65535
        # volume 0 all lights off, volume 10 all lights on.
        last_volume = volume
        volume = range_map(potentiometer.value, 0, 65535, 0, 11)

    if volume != last_volume:
        last_volume = volume
        pixels_to_lit = range_map(volume,0, MAX_VOLUME, 0, NUM_PIXELS)
        pixels[:] = [RED if i < pixels_to_lit else BLACK for i in range(NUM_PIXELS)]
        strip_pixels_to_lit = range_map(volume, 0, MAX_VOLUME, 0, NUM_STRIP_PIXELS)
        strip_pixels[:] = [RED if i < strip_pixels_to_lit else BLACK for i in range(NUM_STRIP_PIXELS)]
        print(f"volume: {volume}, pixels: {pixels_to_lit}, strip_pixels: {strip_pixels_to_lit}")

    sleep(BLINK_DELAY)
