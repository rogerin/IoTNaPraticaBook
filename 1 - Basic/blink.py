"""Pisca um LED conectado ao pino 2 do ESP32 a cada segundo."""

import machine
import time

led = machine.Pin(2, machine.Pin.OUT)


def main() -> None:
    """Liga e desliga o LED em intervalos de 1 segundo."""
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)


if __name__ == "__main__":
    main()
