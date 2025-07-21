"""Monitora vagas de estacionamento e publica via MQTT."""

import machine
from umqtt.simple import MQTTClient
import network


# Configurações de rede e MQTT
CONFIG = {
    "mqtt_broker": "endpoint.iot.us-east-1.amazonaws.com",
    "client_id": "esp32_estacionamento_inteligente",
    "publish_topic": "estacionamento/inteligente/vagas",
    "wifi_ssid": "SeuSSID",
    "wifi_password": "SuaSenha",
    "cert_file": "/certs/certificate.pem.crt",
    "key_file": "/certs/private.pem.key",
    "ca_file": "/certs/ca.pem"
}

def connect_wifi() -> None:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(CONFIG["wifi_ssid"], CONFIG["wifi_password"])
    while not station.isconnected():
        pass
    print("Conectado à Wi-Fi")

def setup_mqtt() -> MQTTClient:
    with open(CONFIG["cert_file"], "rb") as c, open(CONFIG["key_file"], "rb") as k, open(CONFIG["ca_file"], "rb") as ca:
        client = MQTTClient(CONFIG["client_id"], CONFIG["mqtt_broker"], port=8883,
                            ssl=True, ssl_params={"cert": c.read(), "key": k.read(), "ca_certs": ca.read()})
    return client

def main() -> None:
    """Lê o estado das vagas e publica mensagens MQTT."""
    connect_wifi()
    client = setup_mqtt()
    client.connect()

    sensor_pin1 = machine.Pin(14, machine.Pin.IN)
    sensor_pin2 = machine.Pin(15, machine.Pin.IN)

    while True:
        vaga1_status = "Ocupada" if sensor_pin1.value() == 0 else "Livre"
        vaga2_status = "Ocupada" if sensor_pin2.value() == 0 else "Livre"

        # Publica os dados no tópico MQTT
        data = "{},{}".format(vaga1_status, vaga2_status)
        client.publish(CONFIG["publish_topic"], data)

        time.sleep(1)

if __name__ == "__main__":
    main()
