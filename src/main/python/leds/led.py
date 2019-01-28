#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from blinkt import set_pixel, show, set_brightness


class LED(object):
    def __init__(self, index):
        self._index = index
        self._event = None
        self._left = None
        self._right = None
        self._count = 0
        set_brightness(0.20)

    @property
    def index(self):
        return self._index

    @property
    def count(self):
        return self._count

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, val):
        self._event = val

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val):
        self._left = val

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, val):
        self._right = val

    def blink(self, duration=0.5):
        set_pixel(self._index, 0, 0, 255)
        show()
        time.sleep(duration)
        set_pixel(self._index, 0, 0, 0)
        show()
        time.sleep(duration)
        self._count += 1
