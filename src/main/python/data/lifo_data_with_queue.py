#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from random import randrange
from threading import Event
from threading import Lock


class SharedData(object):
    def __init__(self):
        self.__data = None
        self.__lock = Lock()
        self.__queue = Queue(maxsize=1)
        self.__completed = Event()

    @property
    def completed(self):
        with self.__lock:
            return self.__completed.is_set() and self.__queue.qsize() == 0

    def mark_completed(self):
        self.__completed.set()

    def get_data(self):
        # Exit if the producer completed
        if self.completed:
            return None

        with self.__lock:
            try:
                return self.__queue.get(block=False)
            except Empty:
                # Bail if no value is ready to be read
                return None

    def set_data(self, val):
        with self.__lock:
            if self.__queue.full():
                # Empty the queue if item is already present
                discarded = self.__queue.get()
                print("Discarded: {}".format(discarded))
            self.__queue.put(val)


def producer(shared_data):
    for i in range(20):
        shared_data.set_data("image-{0}".format(i))
        # Pause a random amount of time
        time.sleep(randrange(2))
    shared_data.mark_completed()


def consumer(shared_data):
    while not shared_data.completed:
        data = shared_data.get_data()
        if data is not None:
            print(data)
        # Pause a random amount of time
        time.sleep(randrange(3))


def main():
    shared_data = SharedData()
    with ThreadPoolExecutor() as e:
        e.submit(consumer, shared_data, )
        e.submit(producer, shared_data, )


if __name__ == "__main__":
    main()
