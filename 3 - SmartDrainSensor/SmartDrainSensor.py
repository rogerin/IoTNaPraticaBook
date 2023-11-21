import machine
import dht

# Configuração dos pinos
# Pino analógico para o MQ-135
mq135_pin = machine.ADC(machine.Pin(34))
# Pino digital para o DHT11
dht11_pin = machine.Pin(2, machine.Pin.IN)
# Pino digital para o sensor de bueiro
bueiro_pin = machine.Pin(14, machine.Pin.IN)

# Inicialização do sensor DHT11
d = dht.DHT11(dht11_pin)

# Loop principal
while True:
    # Leitura analógica do MQ-135
    mq135_value = mq135_pin.read()
    
    # Realiza a medição do DHT11
    d.measure()
    temperature = d.temperature()
    humidity = d.humidity()
    
    bueiro_status = "Aberto" if bueiro_pin.value() else "Fechado"
    
    print("Valor MQ-135:", mq135_value)
    print("Temperatura:", temperature, "°C")
    print("Umidade:", humidity, "%")
    print("Status do Bueiro:", bueiro_status)
    
    # Aguarda 10 segundos antes da próxima leitura
    time.sleep(10)  
