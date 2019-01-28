#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from leds.led import LED


def main():
    # Setup CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pause", default=0.25, type=float, help="Blink pause (secs) [0.25]")
    args = vars(parser.parse_args())

    # Create LED objects
    leds = [LED(i) for i in range(8)]

    # Blink back and forth
    try:
        while True:
            for led in leds:
                led.blink(args["pause"])

            for led in reversed(leds):
                led.blink(args["pause"])
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
