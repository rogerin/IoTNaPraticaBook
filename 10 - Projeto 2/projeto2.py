import machine
from umqtt.simple import MQTTClient
import network

# Configurações de rede e MQTT
CONFIG = {
    "mqtt_broker": "endpoint.iot.us-east-1.amazonaws.com",
    "client_id": "esp32_bueiro_inteligente",
    "publish_topic": "bueiro/inteligente/dados",
    "wifi_ssid": "SeuSSID",
    "wifi_password": "SuaSenha",
    "cert_file": "/certs/certificate.pem.crt",
    "key_file": "/certs/private.pem.key",
    "ca_file": "/certs/ca.pem"
}

def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(CONFIG["wifi_ssid"], CONFIG["wifi_password"])
    while not station.isconnected():
        pass
    print("Conectado à Wi-Fi")

def setup_mqtt():
    with open(CONFIG["cert_file"], "rb") as c, open(CONFIG["key_file"], "rb") as k, open(CONFIG["ca_file"], "rb") as ca:
        client = MQTTClient(CONFIG["client_id"], CONFIG["mqtt_broker"], port=8883,
                            ssl=True, ssl_params={"cert": c.read(), "key": k.read(), "ca_certs": ca.read()})
    return client

def main():
    connect_wifi()
    client = setup_mqtt()
    client.connect()

    d = dht.DHT11(machine.Pin(2))
    mq135_pin = machine.ADC(machine.Pin(34))
    bueiro_pin = machine.Pin(14, machine.Pin.IN)

    while True:
        mq135_value = mq135_pin.read()
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        bueiro_status = "Aberto" if bueiro_pin.value() else "Fechado"

        # Publica os dados no tópico MQTT
        data = "{},{},{},{}".format(mq135_value, temperature, humidity, bueiro_status)
        client.publish(CONFIG["publish_topic"], data)

        time.sleep(10)

if __name__ == "__main__":
    main()
