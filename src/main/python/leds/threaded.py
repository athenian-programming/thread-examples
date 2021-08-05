#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import random
import time
from leds.led import LED
from threading import Thread
from time import sleep


def execute(led, pause):
    print("Starting thread {0}".format(led.index))
    while not stopped:
        # Pause for a random period of time between 0 and 1 second
        time.sleep(random.random())
        print("Blinking {0}".format(led.index))
        led.blink(pause)
    print("Exiting thread {0}".format(led.index))


def main():
    # Setup CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pause", default=0.5, type=float, help="Blink pause (secs) [0.5]")
    args = vars(parser.parse_args())

    stopped = False

    # Create LED objects
    leds = [LED(j) for j in range(8)]

    # Start threads
    for led in leds:
        t = Thread(target=execute, args=(led, args["pause"]))
        t.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        stopped = True


if __name__ == "__main__":
    main()
