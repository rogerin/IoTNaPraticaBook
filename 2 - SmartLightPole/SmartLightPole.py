"""Controle de intensidade de LED baseado em leitura de LDR."""

import machine
import time

# Configuração dos pinos
# Pino analógico para o LDR
ldr_pin = machine.ADC(machine.Pin(34))
# Pino digital para o LED
led_pin = machine.Pin(2, machine.Pin.OUT)


def main() -> None:
    """Lê o valor do LDR e ajusta o tempo em que o LED fica ligado."""
    while True:
        # Leitura analógica do LDR (0-4095)
        ldr_value = ldr_pin.read()
        # Calcula intensidade normalizada (0-1)
        led_intensity = ldr_value / 4095

        led_pin.value(1)
        time.sleep(led_intensity)
        led_pin.value(0)
        time.sleep(1 - led_intensity)


if __name__ == "__main__":
    main()
