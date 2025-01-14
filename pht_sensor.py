import board
import terminalio
import displayio
import time
from adafruit_display_text import label
import busio
from adafruit_ms8607 import MS8607

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

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

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
text_width = text_area.bounding_box[2] * FONTSCALE
text_group = displayio.Group(
    scale=FONTSCALE,
    x=display.width // 2 - text_width // 2,
    y=display.height // 2,
)
text_group.append(text_area)
splash.append(text_group)

main_group = displayio.Group()
display.root_group = main_group

# create the label
updating_label = label.Label(
    font=terminalio.FONT, text="Time Is:\n{}".format(time.monotonic()), scale=2
)

updating_label.anchor_point = (0, 0)
updating_label.anchored_position = (20, 20)

i2c = busio.I2C(board.SCL, board.SDA)
sensor = MS8607(i2c)

main_group.append(updating_label)

i = 0
while True:
    if i == 0:
        a = ("Pressure: %.2f hPa" % sensor.pressure)
        updating_label.text = (a)
        i += 1
    elif i == 1:
        temp = sensor.temperature
        tempf = 1.8 * temp + 32
        updating_label.text = str (tempf) + " Deg F"
        i += 1
    elif i == 2:
        b = ("Humidity: %.2f %% rH" % sensor.relative_humidity)
        updating_label.text = (b)
        i = 0
    time.sleep(3)
