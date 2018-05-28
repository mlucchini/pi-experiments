import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time


CHANNEL = 0
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


def read_data():
    return mcp.read_adc(CHANNEL)


while True:
    print(read_data())
    time.sleep(0.5)
