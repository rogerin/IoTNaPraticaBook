"""Envia alerta quando o nível de água atinge valor crítico."""

import machine
import time

# Configuração dos pinos
# Pino digital para o sensor de nível de água
water_level_pin = machine.Pin(25, machine.Pin.IN)  

def main() -> None:
    """Monitoramento contínuo do sensor de água."""
    while True:
        water_level = water_level_pin.value()

        if water_level == 1:  # 1 indica nível alto de água
            print("Alerta: Nível de Água Elevado - Possível Enchente")

        time.sleep(300)  # espera 5 minutos


if __name__ == "__main__":
    main()