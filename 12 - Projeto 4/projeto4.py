import time
from machine import Pin, PWM
import network
from umqtt.simple import MQTTClient


# Configurações de rede e MQTT
CONFIG = {
    "mqtt_broker": "endpoint.iot.us-east-1.amazonaws.com",
    "client_id": "esp32_lixeira_inteligente",
    "publish_topic": "lixeira/inteligente/dados",
    "subscribe_topic": "lixeira/inteligente/comando",
    "wifi_ssid": "SeuSSID",
    "wifi_password": "SuaSenha",
    "cert_file": "/certs/certificate.pem.crt",
    "key_file": "/certs/private.pem.key",
    "ca_file": "/certs/ca.pem"
}

# Configuração dos pinos
trigger_pin = Pin(12, Pin.OUT)
echo_pin = Pin(13, Pin.IN)
servo_pin = PWM(Pin(15))

def read_distance():
    trigger_pin.on()
    time.sleep_us(10)
    trigger_pin.off()
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)
    distance = (pulse_duration * 0.0343) / 2
    return distance

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
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(CONFIG["subscribe_topic"])
    return client

def sub_cb(topic, msg):
    print("Received {} under topic {}".format(msg, topic))
    if msg == b'compress':
        servo_pin.duty(512)
        time.sleep(5)
        servo_pin.duty(0)

def main():
    connect_wifi()
    client = setup_mqtt()

    while True:
        distance = read_distance()
        print("Distância:", distance, "cm")
        client.publish(CONFIG["publish_topic"], str(distance))

        client.wait_msg()
        time.sleep(10)

if __name__ == "__main__":
    main()
