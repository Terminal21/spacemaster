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
        GPIO.remove_event_detect(self.channel)
        GPIO.add_event_detect(self.channel,
                              GPIO.RISING,
                              callback=self.switch_rise,
                              bouncetime=150)
        print("switch on")
        self.publisher.send_json(dict(spaceopen=True))

    def switch_rise(self, channel):
        GPIO.remove_event_detect(self.channel)
        GPIO.add_event_detect(self.channel,
                              GPIO.FALLING,
                              callback=self.switch_fall,
                              bouncetime=150)
        print("switch off")
        self.publisher.send_json(dict(spaceopen=False))


    def run(self):
        GPIO.add_event_detect(self.channel,
                              GPIO.FALLING,
                              callback=self.switch_fall,
                              bouncetime=150)
        while True:
            time.sleep(600)

        GPIO.cleanup()


def run():
    spacemaster = Spacemaster()
    spacemaster.run()
