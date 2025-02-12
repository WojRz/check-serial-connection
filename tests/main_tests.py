from check_serial_connection.__main__ import main, Parity


def test_main():
    main(
        port="COM4",
        baudrate=9600,
        bytesize=8,
        parity="NONE",
        stopbits=1,
        timeout=5
    )
