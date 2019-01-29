#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from random import randrange


def consumer(id, queue):
    print("Consumer {} waiting".format(id))
    data = queue.get()
    print("Consumer {} got {}".format(id, data))


def producer(queue, count):
    for i in range(count):
        data = "val-{}".format(i)
        print("Producer put {}".format(data))
        queue.put(data)
        time.sleep(randrange(2))


def main():
    count = 10
    queue = Queue()

    with ThreadPoolExecutor() as executor:
        for i in range(count):
            executor.submit(consumer, i, queue, )
        executor.submit(producer, queue, count, )


if __name__ == "__main__":
    main()
