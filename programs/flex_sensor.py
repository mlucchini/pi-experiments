import os
import spidev
import time


FLEX_SENSOR_CHANNEL = 0
LEFT_DIRECTION = 'LEFT'
RIGHT_DIRECTION = 'RIGHT'


def read_channel():
    return spi.xfer2([1, (8 + FLEX_SENSOR_CHANNEL) << 4, 0])


def read_data():
    adc = read_channel()
    direction = LEFT_DIRECTION if adc[1] == 2 else RIGHT_DIRECTION
    level = adc[2] if direction == RIGHT_DIRECTION else 256 - adc[2]
    return direction, level


spi = spidev.SpiDev()
spi.open(0,0)

while True:
    direction, level = read_data()
    print('-----------------------------')
    print('Flex: {} {}'.format(direction, level))
    time.sleep(0.2)
