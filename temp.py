import time
import board
import pwmio
from analogio import AnalogIn

pot = AnalogIn(board.A0)
x = 0
v = 65535


while True:
    p = pot.value
    a = (p/v) * 3.3
    x = (a-0.5) * 100
    b = x * (1.8) + 32.0
    print(b)
    time.sleep(0.3)


