import machine
import time
from machine import Pin, PWM

# Configuração dos pinos
# Pino de disparo do sensor ultrassônico
trigger_pin = Pin(12, Pin.OUT)
# Pino de eco do sensor ultrassônico
echo_pin = Pin(13, Pin.IN)
# Pino PWM para o servo motor
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

# Loop principal
while True:
    distance = read_distance()
    print("Distância:", distance, "cm")
    
    # Limite de enchimento da lixeira
    if distance < 20: 
        # Aciona o mecanismo de compressão
        servo_pin.duty(512)  
        # Mantém o servo motor acionado por 5 segundos
        time.sleep(5)  
        # Desliga o servo motor
        servo_pin.duty(0) 

    # Aguarda 10 segundos antes da próxima leitura
    time.sleep(10)  