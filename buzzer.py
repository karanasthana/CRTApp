import time
import RPi.GPIO as gpio
def alarm():
    
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(11 ,gpio.OUT)

    num=0
    try:
        while num<1:
            num=num+1
            gpio.output(11,0)
            time.sleep(.55)
            gpio.output(11,1)
            time.sleep(.45)
        gpio.output(11,0)
    except KeyboardInterrupt:
        gpio.cleanup()
        exit


    

alarm()
