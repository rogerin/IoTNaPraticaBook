import machine
# Configuração dos pinos
# Pino digital para o primeiro sensor
sensor_pin1 = machine.Pin(14, machine.Pin.IN)
# Pino digital para o segundo sensor
sensor_pin2 = machine.Pin(15, machine.Pin.IN) 

# Loop principal
while True:
    if sensor_pin1.value() == 0:
        print("Vaga 1 Ocupada")
    else:
        print("Vaga 1 Livre")
    if sensor_pin2.value() == 0:
        print("Vaga 2 Ocupada")
    else:
        print("Vaga 2 Livre")
    
    # Aguarda 1 segundo antes da próxima leitura
    time.sleep(1) 
