import machine
import time

# Configuração dos pinos
# Pino analógico para o LDR
ldr_pin = machine.ADC(machine.Pin(34))
# Pino digital para o LED
led_pin = machine.Pin(2, machine.Pin.OUT)  

# Loop principal
while True:
    # Leitura analógica do LDR
    ldr_value = ldr_pin.read() 
    # Normalização para a faixa do LED (0-1)
    led_intensity = ldr_value / 4095
    
    # Liga o LED
    led_pin.value(1)
    # Mantém o LED ligado proporcionalmente à intensidade lida
    time.sleep(led_intensity)  
    # Desliga o LED
    led_pin.value(0)
    # Mantém o LED desligado proporcionalmente à intensidade lida
    time.sleep(1 - led_intensity)  
