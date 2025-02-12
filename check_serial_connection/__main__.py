import logging
from enum import Enum

import click
import serial

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)


def main(port, baudrate, bytesize, parity, stopbits, timeout):
    logger.info("started")

    connection = {
        'port': port,
        'baudrate': baudrate,
        'bytesize': bytesize,
        'parity': Parity[parity].value,
        'stopbits': stopbits,
        'timeout': timeout
    }

    with serial.Serial(**connection) as ser:
        logger.info(f"made connection: {connection}")
        logger.info("waiting for data")

        x = ser.read()  # read one byte
        s = ser.read(10)  # read up to ten bytes (timeout)
        # line = ser.readline()  # read a '\n' terminated line
        logger.info(s)


class Parity(Enum):
    NONE = 'N'
    EVEN = 'E'
    ODD = 'O'
    MARK = 'M'
    SPACE = 'S'


@click.command()
@click.option("-p", "--port", "port", type=str,
              required=True, help="serial port device name")
@click.option("-b", "--baudrate", "baudrate", type=int,
              required=True, default=9600)
@click.option("-bs", "--bytesize", "bytesize", type=int,
              required=True, default=8)
@click.option("-pa", "--parity", "parity", type=click.Choice(i.name for i in Parity),
              required=True, default="NONE")
@click.option("-sb", "--stopbits", "stopbits", type=float,
              required=True, default=1)
@click.option("-t", "--timeout", "timeout", type=int,
              default=5, help="max time for income data")
def run(**kwargs):
    """Read data from serial device."""
    main(**kwargs)


if __name__ == '__main__':
    run()
