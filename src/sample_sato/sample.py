# -*- coding: utf-8 -*-

import time
import busio
import board
import cv2

# センサドライバ センサ接続時には必要
#import adafruit_amg88xx

# カメラドライバ
import picamera
import picamera.array

# ドロー系ドライバ
import matplotlib.pyplot as plt

# I2Cアクセス系初期設定
i2c_bus = busio.I2C(board.SCL, board.SDA)


#### External library for debug (adafruit_amg88xx.py)) ####
#############################################################################
#### センサ接続＋ドライバimport時は不要 ここから ####

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit, i2c_bits
from micropython import const

_PIXEL_OFFSET = const(0x08)

_PIXEL_ARRAY_WIDTH = const(8)
_PIXEL_ARRAY_HEIGHT = const(8)
_PIXEL_TEMP_CONVERSION = 0.25
_THERMISTOR_CONVERSION = 0.0625


def _signed_12bit_to_float(val):
    # take first 11 bits as absolute val
    abs_val = val & 0x7FF
    if val & 0x800:
        return 0 - float(abs_val)
    return float(abs_val)


def _twos_comp_to_float(val):
    val &= 0xFFF
    if val & 0x800:
        val -= 0x1000
    return float(val)


class AMG88XX:
    """Driver for the AMG88xx GRID-Eye IR 8x8 thermal camera."""

    # Set up the registers
    _pctl = i2c_bits.RWBits(8, 0x00, 0)
    _rst = i2c_bits.RWBits(8, 0x01, 0)
    _fps = i2c_bit.RWBit(0x02, 0)
    _inten = i2c_bit.RWBit(0x03, 0)

    _tthl = i2c_bits.RWBits(8, 0x0E, 0)

    _tthh = i2c_bits.RWBits(4, 0x0F, 0)

    def __init__(self, i2c, addr=0x69):
#        self.i2c_device = I2CDevice(i2c, addr)
        self.i2c_device = 0

        # enter normal mode
#        self._pctl = _NORMAL_MODE

        # software reset
#        self._rst = _INITIAL_RESET

        # disable interrupts by default
#        self._inten = False

        # set to 10 FPS
#        self._fps = _FPS_10

    @property
    def temperature(self):
        """Temperature of the sensor in Celsius"""
        raw = (self._tthh << 8) | self._tthl
        return _signed_12bit_to_float(raw) * _THERMISTOR_CONVERSION

    @property
    def pixels(self):
        """Temperature of each pixel across the sensor in Celsius.

           Temperatures are stored in a two dimensional list where the first index is the row and
           the second is the column. The first row is on the side closest to the writing on the
           sensor."""
        retbuf = [[0] * _PIXEL_ARRAY_WIDTH for _ in range(_PIXEL_ARRAY_HEIGHT)]
        buf = bytearray(3)

#        with self.i2c_device as i2c:
        for row in range(0, _PIXEL_ARRAY_HEIGHT):
            for col in range(0, _PIXEL_ARRAY_WIDTH):
                i = row * _PIXEL_ARRAY_HEIGHT + col
                buf[0] = _PIXEL_OFFSET + (i << 1)
#               i2c.write_then_readinto(buf, buf, out_end=1, in_start=1)
                # <<<<<<<< Dummy data for Debug >>>>>>>> 
                buf[1] = ((col+1) * row)+130
                buf[2] = 0
#                print('buf1:' + str(buf[1]) + ' buf2:' + str(buf[2]), sep='\n')
                # <<<<<<<< Dummy data for Debug >>>>>>>>

                raw = (buf[2] << 8) | buf[1]
                retbuf[row][col] = _twos_comp_to_float(raw) * _PIXEL_TEMP_CONVERSION

        return retbuf

#### センサ接続＋ドライバ import 時は不要ここまで ####
#############################################################################
#### External library for debug (adafruit_amg88xx.py)) ####

# debug counter
count = 0

# Maximize plot window
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
flg = plt.gcf()
flg.canvas.set_window_title('Thermo')

# erase figure
plt.clf()

# main loop

try:
    while True:
    
        # get Sensor value
        sensor = AMG88XX(i2c_bus, addr=0x68)

        # Wait for sensor
        time.sleep(.01)

        # debug print
        print(sensor.pixels)

        # Pick up Maximum Temperature
        max_temp = max(max(sensor.pixels))
        # debug print
#        print(max_temp)

        # Store Picture from Camera
        img0 = cv2.imread('./tmp.jpg')
        # size 
        img = img0[0:640, 0:640]
        img = img[:, :, ::-1].copy()
       
        # erase Figure
        plt.clf()

        # Draw Termography 1 (pure)
        plt.subplot(1,3,1)
        fig = plt.imshow(sensor.pixels, cmap="inferno", vmin=32, vmax=42)
        plt.colorbar(orientation='horizontal')

        # Draw Termography 2 (interpolation)
        plt.subplot(1,3,2)
        fig = plt.imshow(sensor.pixels, cmap="inferno", interpolation="bicubic",vmin=32,vmax=42)
        plt.colorbar(orientation='horizontal')

        # Draw Picture
        plt.subplot(1,3,3)
        plt.imshow(img)

        # Draw text
        plt.text(0, 0, str(max_temp) + ' deg : count ' + str(count), size = 20, color = "red")

        count += 1

#        plt.draw()

        plt.pause(0.01)

# bottom of loop 

        # terminate (by hit [ctrl + C])        
except KeyboardInterrupt:
    print('  *** exit.***')

