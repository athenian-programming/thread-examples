#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from random import randrange
from threading import Event
from threading import Lock
from threading import Thread

from data.timeout_exception import TimeoutException


class SharedData(object):
    def __init__(self):
        self.__data = None
        self.__lock = Lock()
        self.__val_available = Event()
        self.__completed = Event()

    @property
    def completed(self):
        return self.__completed.is_set()

    def mark_completed(self):
        self.__completed.set()

    def get_data(self, timeout_secs=None):
        # Exit if the producer is already completed
        if self.completed:
            return None

        if not self.__val_available.wait(timeout_secs):
            raise TimeoutException
        with self.__lock:
            retval = self.__data
        self.__val_available.clear()
        return retval

    def set_data(self, val):
        with self.__lock:
            self.__data = val
        self.__val_available.set()


def producer(shared_data):
    for i in range(10):
        shared_data.set_data("val-{0}".format(i))
        # Pause a random amount of time
        time.sleep(randrange(2))
    shared_data.mark_completed()


def consumer(shared_data):
    while not shared_data.completed:
        print(shared_data.get_data())
        # Pause a random amount of time
        time.sleep(randrange(2))


def main():
    shared_data = SharedData()
    Thread(target=consumer, args=(shared_data,)).start()
    Thread(target=producer, args=(shared_data,)).start()


if __name__ == "__main__":
    main()
