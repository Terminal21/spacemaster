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

    def publish(open=False):
        print("switch {}".format("on" if open else "off"))
        self.publisher.send_json(dict(sppaceopen=open))

    def run(self):
        guess_gpio = GPIO.HIGH

	while True:
            for i in range(6):
                state_gpio = GPIO.input(self.channel)
                if state_gpio != guess_gpio:
                    guess_gpio = state_gpio
                    self.publish(stat_gpio==GPIO.LOW)
                time.sleep(10)
            self.publish(stat_gpio==GPIO.LOW)

        GPIO.cleanup()


def run():
    spacemaster = Spacemaster()
    spacemaster.run()
