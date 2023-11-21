import machine 
import time 

led = machine.Pin(2, machine.Pin.OUT) 

while True: 
    led.on() 
    time.sleep(1) 
    led.off() 
    time.sleep(1)
