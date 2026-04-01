# AkiPad - KMK Firmware
# Akileash Saravanan

import board
import busio
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.rgb import RGB
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306Driver

keyboard = KMKKeyboard()

# ── Matrix pins ──────────────────────────────────────────────
# Duplex matrix
# Col-0 = D8 = GP2, Col-1 = D2 = GP28
# Row-0 = D3 = GP29, Row-1 = D7 = GP1
keyboard.col_pins = (board.D8, board.D2)
keyboard.row_pins = (board.D3, board.D7)
keyboard.diode_orientation = None  # duplex matrix handles this

# ── Keymap ────────────────────────────────────────────────────
# Layout:
# [ Play/Pause ] [ Next Track ] [ Mute ]
# [ Copy       ] [ Paste      ] [ Undo ]
keyboard.keymap = [
    [
        KC.MPLY,  KC.MNXT,  KC.MUTE,
        KC.COPY,  KC.PASTE, KC.UNDO,
    ]
]

# ── Encoders ─────────────────────────────────────────────────
# Encoder 1: Enc_A = D10 = GP3, Enc_B = D9 = GP4
# Encoder 2: Enc_2A = D0 = GP26, Enc_2B = D1 = GP27
encoder_handler = EncoderHandler()
encoder_handler.pins = (
    (board.D10, board.D9, None, False),   # Encoder 1
    (board.D0,  board.D1, None, False),   # Encoder 2
)
encoder_handler.map = [
    # Layer 0
    (
        (KC.VOLD, KC.VOLU),  # Encoder 1: Volume
        (KC.VOLD, KC.VOLU),  # Encoder 2: Volume
    ),
]
keyboard.modules.append(encoder_handler)

# ── RGB LEDs ─────────────────────────────────────────────────
# LED_DATA = D6 = GP0
rgb = RGB(
    pixel_pin=board.D6,
    num_pixels=6,
    hue_default=0,
    sat_default=255,
    val_default=128,
    animation_mode=AnimationModes.BREATHING,
)
keyboard.extensions.append(rgb)

# ── OLED Display ─────────────────────────────────────────────
# SDA = D4 = GP6, SCL = D5 = GP7
i2c_bus = busio.I2C(board.D5, board.D4)

display = Display(
    display=SSD1306Driver(i2c=i2c_bus, device_address=0x3C),
    entries=[
        TextEntry(text='  AkiPad  ', x=0, y=0),
        TextEntry(text='----------', x=0, y=8),
        TextEntry(text='Akileash  ', x=0, y=16),
        TextEntry(text='Saravanan ', x=0, y=24),
    ],
    width=128,
    height=32,
)
keyboard.extensions.append(display)

# ── Start ─────────────────────────────────────────────────────
if __name__ == '__main__':
    keyboard.go()
