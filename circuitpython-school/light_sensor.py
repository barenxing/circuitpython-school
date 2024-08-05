import board, analogio, time

light_sensor = analogio.AnalogIn(board.LIGHT)

while True:
    print((light_sensor.value,))
    time.sleep(0.2)