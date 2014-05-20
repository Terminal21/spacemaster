import RPi.GPIO as GPIO
import time
import zmq

context = zmq.Context()
publisher = context.socket (zmq.PUB)
publisher.bind ("tcp://*:9000")

channel = 7

def switch_fall(channel):
    GPIO.remove_event_detect(channel)
    GPIO.add_event_detect(channel, GPIO.RISING, callback=switch_rise, bouncetime=150)  
    print("switch on")
    publisher.send_json(dict(spaceopen=True))

def switch_rise(channel):
    GPIO.remove_event_detect(channel)
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=switch_fall, bouncetime=150)  
    print("switch off")
    publisher.send_json(dict(spaceopen=False))


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(channel, GPIO.FALLING, callback=switch_fall, bouncetime=150)  


while True:
    time.sleep(600)

GPIO.cleanup()

