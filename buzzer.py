import time
import RPi.GPIO as gpio
def alarmstart():
    
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(11 ,gpio.OUT)

    try:
        gpio.output(11,1)
        #time.sleep(.45)
    except KeyboardInterrupt:
        gpio.cleanup()
        exit

def shortalarm(num):

    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(11 ,gpio.OUT)
    n=0

    while n<num:
        n=n+2
        try:
            gpio.output(11,1)
            #time.sleep(.45)
        except KeyboardInterrupt:
            gpio.cleanup()
            exit

def alarmstop():
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(11 ,gpio.OUT)

    try:
        gpio.output(11,0)
        #time.sleep(.55)
    except KeyboardInterrupt:
        gpio.cleanup()
        exit




