import RPi.GPIO as GPIO
import logging
import time
import requests

GPIO.cleanup()

class Spacemaster(object):

    publisher = None
    switch = 14
    door = 4

    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setuo(self.door, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        logging.info("SpaceMaster initialized")

    def publish(self, open=False):
        print "publishing"
        if open:
            requests.post('http://putin.local:8888/open', data={'status':'open'})
            requests.post('http://putin.local:8889/open', data={'status':'open'})
        else:
            requests.post('http://putin.local:8888/close', data={'status':'closed'})
            requests.post('http://putin.local:8889/close', data={'status':'closed'})
        print "OK"

    def get_state(self):
        #return (GPIO.input(self.switch) == GPIO.HIGH)
        if (GPIO.input(self.switch) == GPIO.HIGH) and (GPIO.input(self.door) == GPIO.HIGH):
            return False
        return (GPIO.input(self.switch) == GPIO.HIGH)
    
    def run(self):
        last_state = self.get_state()
        self.publish(last_state)
        while True:
            new_state = self.get_state()
            if new_state != last_state:
                last_state = new_state
                self.publish(new_state)
            time.sleep(5)

        logging.info("SpaceMaster died, cleaning up")
        GPIO.cleanup()


def run():
    logformat = "%(asctime)s %(levelname)s [%(name)s][%(threadName)s] %(message)s"
    logging.basicConfig(format=logformat, level=logging.DEBUG)

    spacemaster = Spacemaster()
    spacemaster.run()
