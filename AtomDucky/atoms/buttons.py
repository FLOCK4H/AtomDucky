import digitalio, board
from neopixel import NeoPixel

pixel = NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
button = digitalio.DigitalInOut(board.BTN)