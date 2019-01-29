#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from random import randrange


def consumer(queue, count):
    for i in range(count):
        print("Consumer waiting")
        data = queue.get()
        print("Consumer got {}".format(data))


def producer(queue, count):
    for i in range(count):
        data = "val-{}".format(i)
        print("Producer put {}".format(data))
        queue.put(data)
        time.sleep(randrange(2))


def main():
    count = 10
    manager = Manager()
    queue = manager.Queue()

    with ProcessPoolExecutor() as executor:
        executor.submit(consumer, queue, count, )
        executor.submit(producer, queue, count, )


if __name__ == "__main__":
    main()
