import logging
from enum import Enum

import click
import serial

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(name)s - %(message)s'
)


class ByteSize(Enum):
    FIVEBITS = 5
    SIXBITS = 6
    SEVENBITS = 7
    EIGHTBITS = 8


class Parity(Enum):
    PARITY_NONE = 'N'
    PARITY_EVEN = 'E'
    PARITY_ODD = 'O'
    PARITY_MARK = 'M'
    PARITY_SPACE = 'S'


class StopBits(Enum):
    STOPBITS_ONE = 1
    STOPBITS_ONE_POINT_FIVE = 1.5
    STOPBITS_TWO = 2


@click.command()
@click.option("-p", "--port", "port", type=str,
              required=True, help="serial port device name")
@click.option("-b", "--baudrate", "baudrate", type=int,
              required=True, default=9600)
@click.option("-bs", "--bytesize", "bytesize", type=click.Choice(i.name for i in ByteSize),
              required=True, default="EIGHTBITS")
@click.option("-pa", "--parity", "parity", type=click.Choice(i.name for i in Parity),
              required=True, default="PARITY_NONE")
@click.option("-sb", "--stopbits", "stopbits", type=click.Choice(i.name for i in StopBits),
              required=True, default="STOPBITS_ONE")
@click.option("-t", "--timeout", "timeout", type=int,
              default=5, help="max time for income data")
def main(port, baudrate, bytesize, parity, stopbits, timeout):
    """Read data from serial device."""
    logger.info("started")

    connection = {
        'port': port,
        'baudrate': baudrate,
        'bytesize': ByteSize[bytesize].value,
        'parity': Parity[parity].value,
        'stopbits': StopBits[stopbits].value,
        'timeout': timeout
    }

    with serial.Serial(**connection) as ser:
        logger.info(f"made connection: {connection}")
        logger.info("waiting for data")

        x = ser.read()  # read one byte
        s = ser.read(10)  # read up to ten bytes (timeout)
        # line = ser.readline()  # read a '\n' terminated line
        print(s)


if __name__ == '__main__':
    main()
