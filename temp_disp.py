import time
import board
import pwmio
from analogio import AnalogIn
import displayio
import terminalio
from adafruit_display_text import label

pot = AnalogIn(board.A0)
x = 0
v = 65535

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon
# First set some parameters used for shapes and text
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0xFFFFFF
FOREGROUND_COLOR = 0x000000
TEXT_COLOR = 0xFFFFFF
WHITE = 0xFFFFFF
BACKGROUND = 0XFF0000

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D3
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

splash = displayio.Group()
display.root_group = splash
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR


bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
main_group = displayio.Group()
display.root_group = main_group
splash.append(inner_sprite)
updating_label = label.Label(
    font=terminalio.FONT, text="Time Is:\n{}".format(time.monotonic()), scale=3
)

updating_label.anchor_point = (0, 0)
updating_label.anchored_position = (20, 20)

main_group.append(updating_label)
while True:
    p = pot.value
    a = (p/v) * 3.3
    x = (a-0.5) * 100
    b = x * (1.8) + 32.0
    t = round(b, 2)
    print(t)
    time.sleep(0.1)
    text = str(t) + " Deg F"
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    updating_label.text = str(text).format(time.monotonic())
    time.sleep(1)

    

