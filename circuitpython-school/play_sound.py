import board, neopixel, digitalio, time
from adafruit_led_animation.color import BLACK, BLUE, RED

from adafruit_debouncer import Button
from audiocore import WaveFile

# support for Circuit Playground Express or BlueFruit
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        print("This board does not support audio")


PIXEL_COUNT = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, PIXEL_COUNT)
pixels.brightness = 0.1
pixels.fill(BLACK)

button_A_pin = digitalio.DigitalInOut(board.BUTTON_A)
button_A_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(button_A_pin, value_when_pressed=True)

button_B_pin = digitalio.DigitalInOut(board.BUTTON_B)
button_B_pin.switch_to_input(pull=digitalio.Pull.DOWN)
button_B = Button(button_B_pin, value_when_pressed=True)

speaker_pin = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_pin.direction = digitalio.Direction.OUTPUT
speaker_pin.value = True

audio = AudioOut(board.SPEAKER)
PATH = "drumSounds/"
BUTTON_A_WAV = "drum_cowbell.wav"
BUTTON_B_WAV = "scratch.wav"


def pulse() -> None:
    for i in range(101):
        pixels.brightness = i/100
    for i in range(100, -1, -1):
        pixels.brightness = i/100


def play_sound(filename: str) -> None:
    with open(PATH+filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass


while True:
    button_A.update()
    button_B.update()

    if button_A.pressed:
        play_sound(BUTTON_B_WAV)
        pulse()
    if button_B.pressed:
        pixels.fill(BLACK)

