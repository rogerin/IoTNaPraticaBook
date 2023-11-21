import machine
import time

# Configuração dos pinos
# Pino digital para o sensor de nível de água
water_level_pin = machine.Pin(25, machine.Pin.IN)  

# Loop principal
while True:
    # Leitura do sensor de nível de água
    water_level = water_level_pin.value() 

    # Nível de água alto (possível enchente)
    if water_level == 1:
        print("Alerta: Nível de Água Elevado - Possível Enchente")
    
    # Aguarda 5 minutos antes da próxima leitura
    time.sleep(300)  