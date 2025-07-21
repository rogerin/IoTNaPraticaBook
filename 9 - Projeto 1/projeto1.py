"""Publica a intensidade de luz de um poste inteligente via MQTT."""

import machine
import time
from umqtt.simple import MQTTClient
import network

# Configurações da rede e MQTT
CONFIG = {
    "mqtt_broker": "endpoint.iot.us-east-1.amazonaws.com",
    "client_id": "esp32_poste_inteligente",
    "publish_topic": "poste/inteligente/luminosidade",
    "subscribe_topic": "poste/inteligente/comando",
    "wifi_ssid": "SeuSSID",
    "wifi_password": "SuaSenha",
    "cert_file": "/certs/certificate.pem.crt",
    "key_file": "/certs/private.pem.key",
    "ca_file": "/certs/ca.pem"
}

def connect_wifi(ssid: str, password: str) -> None:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print("Conectado à Wi-Fi")

def sub_callback(topic, msg) -> None:
    """Lida com mensagens recebidas para acionar o LED."""
    print((topic, msg))
    if topic == bytes(CONFIG["subscribe_topic"], 'utf-8') and msg == b'on':
        led_pin.value(1)
    elif topic == bytes(CONFIG["subscribe_topic"], 'utf-8') and msg == b'off':
        led_pin.value(0)

def main() -> None:
    """Configura o MQTT e envia a intensidade de luz periodicamente."""
    connect_wifi(CONFIG["wifi_ssid"], CONFIG["wifi_password"])
    
    with open(CONFIG["cert_file"], "rb") as c, open(CONFIG["key_file"], "rb") as k, open(CONFIG["ca_file"], "rb") as ca:
        client = MQTTClient(client_id=CONFIG["client_id"],
                            server=CONFIG["mqtt_broker"],
                            port=8883,
                            keepalive=5000,
                            ssl=True,
                            ssl_params={"cert": c.read(), "key": k.read(), "ca_certs": ca.read(), "server_side": False})
    
    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(CONFIG["subscribe_topic"])

    ldr_pin = machine.ADC(machine.Pin(34))
    led_pin = machine.Pin(2, machine.Pin.OUT)

    try:
        while True:
            ldr_value = ldr_pin.read()
            led_intensity = ldr_value / 4095
            client.publish(CONFIG["publish_topic"], str(led_intensity))
            time.sleep(5)
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
