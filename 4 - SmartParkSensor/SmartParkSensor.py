"""Verifica ocupação de vagas usando dois sensores digitais."""

import machine
import time
# Configuração dos pinos
# Pino digital para o primeiro sensor
sensor_pin1 = machine.Pin(14, machine.Pin.IN)
# Pino digital para o segundo sensor
sensor_pin2 = machine.Pin(15, machine.Pin.IN)

def main() -> None:
    """Exibe o status das duas vagas de estacionamento."""
    while True:
        if sensor_pin1.value() == 0:
            print("Vaga 1 Ocupada")
        else:
            print("Vaga 1 Livre")

        if sensor_pin2.value() == 0:
            print("Vaga 2 Ocupada")
        else:
            print("Vaga 2 Livre")

        time.sleep(1)


if __name__ == "__main__":
    main()
