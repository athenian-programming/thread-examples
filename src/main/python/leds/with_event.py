#!/usr/bin/env python2

import argparse
from leds.led import LED
from threading import Event
from threading import Thread
from time import sleep


def execute(led, reverse, pause):
    print("Starting thread {0}".format(led.index))
    while not stopped:
        # Wait until someone calls led.event.set()
        led.event.wait()
        led.event.clear()

        print("Blinking {0}".format(led.index))
        led.blink(pause)

        next = led.left if reverse else led.right
        print("Setting {0}".format(next.index))
        next.event.set()

    print("Exiting thread {0}".format(led.index))


# Setup CLI args
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--pause", default=0.05, type=float, help="Blink pause (secs) [0.05]")
parser.add_argument("-r", "--reverse", default=False, action="store_true", help="Reverse blink direction [false]")
args = vars(parser.parse_args())

stopped = False

# Create LED objects
leds = [LED(j) for j in range(8)]

# Assign neighbors to each led -- leds on end wrap around
for i, led in enumerate(leds):
    led.event = Event()
    led.left = leds[i - 1] if i > 0 else leds[7]
    led.right = leds[i + 1] if i < 7 else leds[0]

# Start threads
for led in leds:
    t = Thread(target=execute, args=(led, args["reverse"], args["pause"]))
    t.start()

# Prime the pump
leds[0].event.set()

try:
    while True:
        sleep(60)
except KeyboardInterrupt:
    stopped = True
    print("Exiting...")
