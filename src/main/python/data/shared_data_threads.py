#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from threading import Event
from threading import Lock

from data.timeout_exception import TimeoutException


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

    def get_data(self, timeout_secs=None):
        # Exit if the producer is already completed
        if self.completed:
            return None

        # Wait for value to be ready
        if not self.__value_available.wait(timeout_secs):
            raise TimeoutException

        with self.__lock:
            retval = self.__data

        self.__value_available.clear()
        self.__value_read.set()
        return retval

    def set_data(self, val, timeout_secs=None):
        # Wait for value to be consumed
        if not self.__value_read.wait(timeout_secs):
            raise TimeoutException
        else:
            with self.__lock:
                self.__data = val

            self.__value_read.clear()
            self.__value_available.set()


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
    with ThreadPoolExecutor(max_workers=3) as e:
        e.submit(consumer, shared_data, )
        e.submit(producer, shared_data, )

if __name__ == "__main__":
    main()
