# play_mp3_bluefruit.py
# For Circuit Playground Bluefruit only

import board
import digitalio
from adafruit_debouncer import Button
from audiomp3 import MP3Decoder
from audiopwmio import PWMAudioOut as AudioOut

speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

audio = AudioOut(board.SPEAKER)

mp3_files = ["encouragement1.mp3", "encouragement2.mp3", "nice-work.mp3"]
mp3_count = len(mp3_files)
mp3_play_index = 0


# Because creating an MP3Decoder object takes a lot of memory,
# it's best to do this just once when your program starts,
# and then update the .file property of the MP3Decoder when
# you want to play a different file.  Otherwise, you may encounter
# the dreaded MemoryError.
path = "sounds/"
mp3 = open(path+mp3_files[0], "rb")
decoder = MP3Decoder(mp3)

button_A_input = digitalio.DigitalInOut(board.BUTTON_A)
button_A_input.switch_to_input(pull=digitalio.Pull.DOWN)
button_A = Button(pin=button_A_input, value_when_pressed=True)


def play_mp3(filename):
    decoder.file = open(path+filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass


while True:
    button_A.update()
    if button_A.pressed:
        # print("Button A pressed")
        play_mp3(mp3_files[mp3_play_index])
        mp3_play_index = (mp3_play_index + 1) % mp3_count
