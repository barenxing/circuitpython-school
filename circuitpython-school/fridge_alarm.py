import board, neopixel, digitalio, analogio
from time import sleep
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

light_sensor = analogio.AnalogIn(board.LIGHT)

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
PATH = "alarm/"
SOUND_FILE = "siren.wav"

armed = False

def pulse() -> bool:
    pixels.fill(RED)
    for i in range(101):
        pixels.brightness = i / 100
        button_B.update()
        if button_B.pressed:
            return False
    for i in range(100, -1, -1):
        pixels.brightness = i / 100
        button_B.update()
        if button_B.pressed:
            return False
    return True


def play_sound(filename: str) -> bool:
    with open(PATH + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            keep_playing = pulse()
            if not keep_playing:
                pixels.fill(BLACK)
                pixels.brightness = 0.0
                audio.stop()
        return keep_playing

print("Press Button A to arm the fridge alarm...")
while True:
    button_A.update()

    if button_A.pressed:
        print("Activating alarm, you have 5 seconds to close the fridge door...")
        for i in range(5, 0, -1):
            print(i, end=", ")
            sleep(1)
        print("0... Alarm armed.")
        armed = True

    if armed and light_sensor.value > 3000:
        armed = play_sound(SOUND_FILE)
