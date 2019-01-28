#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from threading import Lock
from threading import Thread
from time import sleep

from leds.led import LED


def execute(led, leds, pause, fair):
    print("Starting thread {0}".format(led.index))
    while not stopped:
        with lock:
            if fair and led.count != min([l.count for l in leds]):
                continue
            led.blink(pause)
            print("Blinks: {0}".format([l.count for l in leds]))
    print("Exiting thread {0}".format(led.index))


def main():
    # Setup CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pause", default=0.05, type=float, help="Blink pause (secs) [0.05]")
    parser.add_argument("-f", "--fair", default=False, action="store_true", help="Blink fairly [false]")
    args = vars(parser.parse_args())

    stopped = False
    lock = Lock()

    # Create LED objects
    leds = [LED(j) for j in range(8)]

    # Start threads
    for i, led in enumerate(leds):
        t = Thread(target=execute, args=(leds[i], leds, args["pause"], args["fair"]))
        t.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        stopped = True
        print("Exiting...")


if __name__ == "__main__":
    main()
