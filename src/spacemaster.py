import RPi.GPIO as GPIO
import logging
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
        logging.info("SpaceMaster initialized")

    def publish(self, open=False):
        logging.info("switch is {}".format("on" if open else "off"))
        self.publisher.send_json(dict(spaceopen=open))

    def run(self):
        guess_gpio = GPIO.HIGH

	while True:
            for i in range(6):
                state_gpio = GPIO.input(self.channel)
                if state_gpio != guess_gpio:
                    guess_gpio = state_gpio
                    self.publish(state_gpio==GPIO.LOW)
                time.sleep(10)
            self.publish(state_gpio==GPIO.LOW)

        logging.info("SpaceMaster died, cleaning up")
        GPIO.cleanup()


def run():
    logformat = "%(asctime)s %(levelname)s [%(name)s][%(threadName)s] %(message)s"
    logging.basicConfig(format=logformat, level=logging.DEBUG)

    spacemaster = Spacemaster()
    spacemaster.run()
