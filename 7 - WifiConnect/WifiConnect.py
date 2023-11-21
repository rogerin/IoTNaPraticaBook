import network

# Configurações da rede Wi-Fi
SSID = 'NomeDaRedeWiFi'
PASSWORD = 'SenhaDaRedeWiFi'

# Função para conectar à rede Wi-Fi
def connect_to_wifi():
    wifi = network.WLAN(network.STA_IF)  # Modo Estação (Cliente)
    
    if not wifi.isconnected():
        print('Conectando à rede Wi-Fi...')
        wifi.active(True)
        wifi.connect(SSID, PASSWORD)
        
        while not wifi.isconnected():
            pass
        
    print('Conectado à rede Wi-Fi')
    print('IP:', wifi.ifconfig()[0])

# Chamada da função para conectar à rede Wi-Fi
connect_to_wifi()
