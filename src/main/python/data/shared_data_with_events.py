#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from threading import Event
from threading import Lock


class SharedData(object):
    def __init__(self):
        self.__data = None
        self.__lock = Lock()
        self.__value_available = Event()
        self.__value_read = Event()
        self.__completed = Event()

        # Prime reader_ready with ready to not block producer
        self.__value_read.set()

    @property
    def completed(self):
        return self.__completed.is_set()

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        # Wait for value to be ready
        if not self.__value_available.wait(timeout=1):
            return None

        with self.__lock:
            retval = self.__data

        self.__value_available.clear()
        self.__value_read.set()
        return retval

    def set_data(self, val):
        # Wait for value to be consumed
        self.__value_read.wait()

        with self.__lock:
            self.__data = val

        self.__value_read.clear()
        self.__value_available.set()


def producer(shared_data):
    for i in range(20):
        data = "val-{0}".format(i)
        shared_data.set_data(data)
        # Pause a random amount of time
        time.sleep(randrange(2))
    shared_data.mark_completed()


def consumer(shared_data):
    while not shared_data.completed:
        data = shared_data.get_data()
        if data is not None:
            print(data)
        # Pause a random amount of time
        time.sleep(randrange(2))


def main():
    shared_data = SharedData()
    with ThreadPoolExecutor() as executor:
        executor.submit(consumer, shared_data, )
        executor.submit(producer, shared_data, )


if __name__ == "__main__":
    main()
