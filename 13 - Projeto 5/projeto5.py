"""Sensor de nível de água que envia alertas MQTT."""

import machine
import time
from umqtt.simple import MQTTClient
import network

# Configurações de rede e MQTT
CONFIG = {
    "mqtt_broker": "endpoint.iot.us-east-1.amazonaws.com",
    "client_id": "esp32_sensor_agua_inteligente",
    "publish_topic": "agua/inteligente/alertas",
    "wifi_ssid": "SeuSSID",
    "wifi_password": "SuaSenha",
    "cert_file": "/certs/certificate.pem.crt",
    "key_file": "/certs/private.pem.key",
    "ca_file": "/certs/ca.pem"
}

def connect_wifi() -> None:
    """ Estabelece conexão Wi-Fi. """
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(CONFIG["wifi_ssid"], CONFIG["wifi_password"])
    while not station.isconnected():
        pass
    print("Conectado à Wi-Fi")

def setup_mqtt() -> MQTTClient:
    """ Configura o cliente MQTT com segurança SSL e retorna o cliente. """
    with open(CONFIG["cert_file"], "rb") as c, open(CONFIG["key_file"], "rb") as k, open(CONFIG["ca_file"], "rb") as ca:
        client = MQTTClient(CONFIG["client_id"], CONFIG["mqtt_broker"], port=8883,
                            ssl=True, ssl_params={"cert": c.read(), "key": k.read(), "ca_certs": ca.read()})
    client.connect()
    return client

def main() -> None:
    """ Função principal para monitoramento de nível de água e envio de alertas. """
    connect_wifi()
    client = setup_mqtt()

    # Configuração do pino do sensor de nível de água
    water_level_pin = machine.Pin(25, machine.Pin.IN)

    while True:
        water_level = water_level_pin.value()
        # Checa o nível de água e envia um alerta se estiver alto
        if water_level == 1:
            message = "Alerta: Nível de Água Elevado – Possível Enchente"
            client.publish(CONFIG["publish_topic"], message)
            print("Alerta enviado!")

        # Aguarda 5 minutos antes da próxima leitura
        time.sleep(300)

if __name__ == "__main__":
    main()
