import RPi.GPIO as GPIO
import time
import zmq

context = zmq.Context()
publisher = context.socket (zmq.PUB)
publisher.bind ("tcp://*:9000")


def switch_fall():
    print("switch on")
    publisher.send_json(dict(spaceopen=True))

def switch_rise():
    print("switch off")
    publisher.send_json(dict(spaceopen=False))


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(7, GPIO.FALLING, callback=switch_fall, bouncetime=150)  
GPIO.add_event_detect(7, GPIO.RISING, callback=switch_rise, bouncetime=150)  


while True:
    time.sleep(1)
    
GPIO.cleanup()
