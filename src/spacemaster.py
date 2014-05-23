import RPi.GPIO as GPIO
import time
import zmq

class Spacemaster(object):

    publisher = None
    channel = 7

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        context = zmq.Context()
        self.publisher = context.socket (zmq.PUB)
        self.publisher.bind ("tcp://*:9000")


    def switch_fall(self, channel):
        print("switch on")
        self.publisher.send_json(dict(spaceopen=True))

    def switch_rise(self, channel):
        print("switch off")
        self.publisher.send_json(dict(spaceopen=False))

    def run(self):
        guess_gpio = GPIO.HIGH

        while True:
            state_gpio = GPIO.input(channel)
            if state_gpio != guess_gpio:
                guess_gpio = state_gpio
                if state_gpio == GPIO.LOW:
                    self.switch_fall(channel)
                else:
                    self.switch_rise(channel)
            
            time.sleep(10)

        GPIO.cleanup()


def run():
    spacemaster = Spacemaster()
    spacemaster.run()
