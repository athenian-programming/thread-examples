#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from random import randrange
from threading import Event
from threading import Lock


class EventContext(object):
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


def consumer(context):
    while not context.completed:
        data = context.get_data()
        if data is not None:
            print("Consumed {}".format(data))
        # Pause a random amount of time
        time.sleep(randrange(2))
    print("Consumer finished")


def producer(context, count):
    for i in range(count):
        data = "val-{0}".format(i)
        print("Put {}".format(data))
        context.set_data(data)
        # Pause a random amount of time
        time.sleep(randrange(2))
    context.mark_completed()
    print("Producer finished")


def main():
    count = 10
    context = EventContext()

    with ThreadPoolExecutor() as executor:
        executor.submit(consumer, context, )
        executor.submit(producer, context, count, )


if __name__ == "__main__":
    main()
