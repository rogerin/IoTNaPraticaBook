"""Exemplo de envio de leituras de um LDR para o AWS IoT Core via MQTT."""

import machine
import time
from umqtt.simple import MQTTClient
import network

# Configurações do AWS IoT Core
# Substitua pelas suas informações de endpoint e tópico
AWS_ENDPOINT = "your-aws-endpoint"
CLIENT_ID = "your-client-id"
TOPIC = "your/topic"

# Certificados e chaves para autenticação TLS
CERT_FILE = "/path/to/certfile.crt"
KEY_FILE = "/path/to/keyfile.key"

# Conecta ao Wi-Fi
def connect_wifi() -> None:
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando ao Wi-Fi...')
        sta_if.active(True)
        sta_if.connect('your-SSID', 'your-password')
        while not sta_if.isconnected():
            pass
    print('Conexão Wi-Fi estabelecida.')

# Configura o MQTT
def setup_mqtt() -> MQTTClient:
    """Configura o cliente MQTT utilizando certificados locais."""
    client = MQTTClient(
        CLIENT_ID, 
        AWS_ENDPOINT, 
        keepalive=5000, 
        ssl=True, 
        ssl_params={
            "cert": CERT_FILE, 
            "key": KEY_FILE, 
            "server_side": False
        }
    )
    client.connect()
    return client

# Configuração dos pinos
# Pino analógico para o LDR
ldr_pin = machine.ADC(machine.Pin(34))
# Pino digital para o LED
led_pin = machine.Pin(2, machine.Pin.OUT)

def main() -> None:
    """Envia leituras do LDR para o AWS IoT Core continuamente."""
    connect_wifi()
    mqtt_client = setup_mqtt()

    while True:
        ldr_value = ldr_pin.read()
        led_intensity = ldr_value / 4095
        led_pin.value(1)
        time.sleep(led_intensity)
        led_pin.value(0)
        time.sleep(1 - led_intensity)

        payload = '{{"ldr_value": {}}}'.format(ldr_value)
        mqtt_client.publish(TOPIC, payload)
        print('Dados enviados: ' + payload)


if __name__ == "__main__":
    main()