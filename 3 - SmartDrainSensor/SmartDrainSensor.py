"""Monitora qualidade do ar e condições do bueiro via ESP32."""

import machine
import dht
import time

# Configuração dos pinos
# Pino analógico para o MQ-135
mq135_pin = machine.ADC(machine.Pin(34))
# Pino digital para o DHT11
dht11_pin = machine.Pin(2, machine.Pin.IN)
# Pino digital para o sensor de bueiro
bueiro_pin = machine.Pin(14, machine.Pin.IN)

# Inicialização do sensor DHT11
d = dht.DHT11(dht11_pin)

def main() -> None:
    """Realiza leituras de sensores e exibe os valores a cada 10 segundos."""
    while True:
        mq135_value = mq135_pin.read()

        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()

        bueiro_status = "Aberto" if bueiro_pin.value() else "Fechado"

        print("Valor MQ-135:", mq135_value)
        print("Temperatura:", temperature, "°C")
        print("Umidade:", humidity, "%")
        print("Status do Bueiro:", bueiro_status)

        time.sleep(10)


if __name__ == "__main__":
    main()
