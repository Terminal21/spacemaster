import RPi.GPIO as GPIO
import time
import zmq

context = zmq.Context()
publisher = context.socket (zmq.PUB)
publisher.bind ("tcp://*:9000")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
message = dict(spaceopen = None)

while True:
    try:
        GPIO.wait_for_edge(7, GPIO.FALLING)
        print("switch on")
        message['spaceopen'] = True
        publisher.send_json(message)
        time.sleep(0.1)
        GPIO.wait_for_edge(7, GPIO.RISING)
        print("switch off")
        message['spaceopen'] = False
        publisher.send_json(message)
        time.sleep(0.1)
    except KeyBoardInterrupt:
        GPIO.cleanup()
GPIO.cleanup()
